#include <iostream>
#include <vector>
#include <chrono>


long long fibonacci(int n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

long long calculateMatrixSum(const std::vector<std::vector<int>>& matrix) {
    long long sum = 0;
    for (int i = 0; i < matrix.size(); ++i) {
        for (int j = 0; j < matrix[i].size(); ++j) {
            sum += matrix[i][j];
        }
    }
    return sum;
}   

int main() {
    std::cout << "Start computation..." << std::endl;

    auto start = std::chrono::high_resolution_clock::now();
    long long fib_result = fibonacci(30);
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> duration = end - start;
    std::cout << "Fibonacci(30) = " << fib_result << " calculated in " << duration.count() << " seconds." << std::endl;

    int rows = 10000, cols = 1000;
    std::vector<std::vector<int>> matrix(rows, std::vector<int>(cols, 1));

    start = std::chrono::high_resolution_clock::now();
    long long matrix_sum = calculateMatrixSum(matrix);
    end = std::chrono::high_resolution_clock::now();
    duration = end - start;
    std::cout << "Matrix sum = " << matrix_sum << " calculated in " << duration.count() << " seconds." << std::endl;

    fibonacci(30);
    fibonacci(31);
    fibonacci(32);

    calculateMatrixSum(matrix);
    calculateMatrixSum(matrix);

    return 0;
}
