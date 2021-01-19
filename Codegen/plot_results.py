#!/usr/bin/python3

import matplotlib.pyplot as plt
plt.style.use('ggplot')
import os
import argparse

width = 0.15

def plot(sizes, dirname, prefix, color, index):
    gflops = []
    for size in sizes:
        file_name = dirname + '/matmul_' + size + '_%s_perf.out'%prefix
        try:
            with open(file_name, 'r') as f:
                speed = f.readlines()
            gflops.append(float(speed[0].split()[0]))
        except:
            gflops.append(0.0)

    x_pos = [i + index * width for i, _ in enumerate(sizes)]
    plt.bar(x_pos, gflops, width, color=color, label=prefix)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-matrix_sizes', dest='matrix_sizes', action='store',
                        help='Path to file containing matrix sizes', default='benchmark_sizes.txt')
    parser.add_argument('-mkl_dir', dest='mkl_dir', action='store',
                        help='Path to MKL performance results', default='mkl/')
    parser.add_argument('-mlir_dir', dest='mlir_dir', action='store',
                        help='Path to MLIR performance results', default='build/matmul/')
    parser.add_argument('-openblas_dir', dest='openblas_dir', action='store',
                        help='Path to OpenBLAS performance results', default='openblas/')
    args = parser.parse_args()

    sizes = None
    with open(args.matrix_sizes, 'r') as f:
        sizes = f.read().splitlines()

    dirs = [args.mkl_dir, args.mlir_dir, args.openblas_dir]
    labels = ['mkl', 'mlir', 'openblas']
    colors = ['r', 'g', 'b']

    for i in range(len(labels)):
        plot(sizes, dirs[i], labels[i], colors[i], i)

    plt.xlabel("Matrix sizes")
    plt.ylabel("GFLOPS")
    plt.title("Single Precision Matrix Multiplication")
    x_pos = [i + width for i, _ in enumerate(sizes)]
    plt.xticks(x_pos, sizes, rotation=90, fontsize=5)
    plt.legend(loc='best')
    plt.savefig('matmul.png', dpi=300, bbox_inches='tight')
