import subprocess
import time

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import os
import re
import openai

app = Flask(__name__)
cors = CORS(app)

openai.api_key = ''

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = 'sunt-smecher'

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.source_file = 'main.cpp'


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        message = response['choices'][0]['message']['content']
        return jsonify({'response': message})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/upload_source', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    # If no file is selected, return an error
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    app.source_file = file.filename
    # Save the file to the server
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    return jsonify({'message': f'File successfully uploaded to {file_path}'}), 200


@app.route("/run_source_file", methods=['GET'])
def run_source_file():
    command = "cmake --build ./build"
    try:
        # Run the command using subprocess
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        time.sleep(10)

        with open('build/vtune_results_/hotspots_report.txt', 'r') as f:
            lines = f.readlines()

        results = []

        for line in lines:
            # Skip headers and dividers
            if line.strip() == '' or line.startswith('Function') or line.startswith('-'):
                continue

            # Split line using 2 or more spaces as delimiter
            parts = re.split(r'\s{2,}', line.strip())

            if len(parts) >= 9:
                cpu_time = parts[1]  # CPU Time is the second column
                start_address = parts[-1]  # Start Address is the last column
                results.append((cpu_time, start_address))

        # Return the command output
        if result.returncode == 0:
            return jsonify({'message': 'Command executed successfully', 'output': results}), 200
        else:
            return jsonify({'error': 'Command failed', 'stderr': result.stderr}), 500
    except Exception as e:
        return jsonify({'error': f'Error executing command: {str(e)}'}), 500



if __name__ == "__main__":
    app.run(debug=True)