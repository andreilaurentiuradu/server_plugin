import subprocess
import time

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import os
import re
app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = 'sunt-smecher'

UPLOAD_FOLDER = '.'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.source_file = 'main.cpp'

@app.route('/')
def index():
    return {"value": "hello world"}


@app.route('/upload_source', methods=['POST'])
def upload_file():
    file = request.files.get('file')

    if file and file.filename:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
    else:
        return 'No file uploaded', 400

    command = "cmake --build ./build"
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)

        with open('build/vtune_results_/hotspots_report.txt', 'r') as f:
            lines = f.readlines()

        results = []

        # Module externe (DLL-uri Windows, runtime)
        excluded_modules = [
            'ucrtbased.dll', 'ucrtbase.dll', 'ntdll.dll', 'msvcrt.dll',
            'kernel32.dll', 'vcruntime140.dll', 'vcruntime140_1.dll',
            'libcmt.lib', 'libucrt.lib'
        ]

        # Header-e STL și fișiere non-proprii
        excluded_sources = [
            '[Unknown]', 'vector', 'xutility', 'memory', 'string', 'algorithm',
            'iterator', 'functional', 'type_traits', 'initializer_list',
            'stdexcept', 'new', 'map', 'unordered_map', 'set', 'list',
            'array', 'deque', 'numeric', 'limits', 'ios', 'streambuf', 'locale'
        ]

        for line in lines:
            if line.strip() == '' or line.startswith('Function') or line.startswith('-'):
                continue

            parts = re.split(r'\s{2,}', line.strip())
            if len(parts) >= 9:
                source_file = parts[-2]
                module = parts[-3]

                # Verificăm că e .cpp (nu .h sau STL)
                if not source_file.endswith('.cpp'):
                    continue

                # Eliminăm dacă e din modul extern
                if any(ex_mod.lower() in module.lower() for ex_mod in excluded_modules):
                    continue

                # Eliminăm dacă fișierul sursă e STL sau necunoscut
                if any(ex_src in source_file for ex_src in excluded_sources):
                    continue

                cpu_time = parts[1]
                start_address = parts[-1]
                function_name = parts[0]

                results.append({
                    "function": function_name,
                    "cpu_time": cpu_time,
                    "start_address": start_address
                })
        print(results)
        if result.returncode == 0:
            return jsonify({'message': 'Command executed successfully', 'value': results}), 200
        else:
            return jsonify({'error': 'Command failed', 'stderr': result.stderr}), 500

    except Exception as e:
        return jsonify({'error': f'Error executing command: {str(e)}'}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)