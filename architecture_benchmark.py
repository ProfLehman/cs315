import hashlib
import math
import os
import platform
import sys
import time
from concurrent.futures import ProcessPoolExecutor

TEST_SECONDS = 20
WORKERS = min(os.cpu_count() or 2, 8)
MIB = 1024 * 1024
FLOAT_ITERATIONS = 20_000


def timed_test(task, seconds=TEST_SECONDS):
    start = time.perf_counter()
    repetitions = 0
    result = None
    while time.perf_counter() - start < seconds:
        result = task()
        repetitions += 1
    return repetitions, time.perf_counter() - start, result


def floating_point():
    x = 1.0
    for i in range(1, FLOAT_ITERATIONS + 1):
        x = x * 1.0000001 + math.sin(i) / (i + 1)
    return x


def worker_float(seconds):
    repetitions, elapsed, value = timed_test(floating_point, seconds)
    return repetitions * FLOAT_ITERATIONS, elapsed, value


def main():
    print('Python 3 Computer Architecture Benchmark', flush=True)
    print(f'OS: {platform.platform()}')
    print(f'Architecture: {platform.machine()}')
    print(f'Logical CPUs reported: {os.cpu_count()}')
    print(f'Python: {sys.version.split()[0]}')
    print(f'Workers for multicore test: {WORKERS}')
    print(f'Time per test: approximately {TEST_SECONDS} seconds\n', flush=True)

    print('1. Single-process floating point...', flush=True)
    ops, elapsed, _ = worker_float(TEST_SECONDS)
    single_rate = ops / elapsed
    print(f'   {single_rate:,.0f} iterations/second\n', flush=True)

    print('2. Memory copy (64 MiB blocks)...', flush=True)
    source = bytes(64 * MIB)
    destination = bytearray(64 * MIB)

    def copy_memory():
        destination[:] = source
        return destination[0]

    repetitions, elapsed, _ = timed_test(copy_memory)
    print(f'   {repetitions * 64 / elapsed:,.0f} MiB/second\n', flush=True)
    del source, destination

    print('3. SHA-256 (8 MiB blocks)...', flush=True)
    data = b'x' * (8 * MIB)

    def hash_data():
        return hashlib.sha256(data).digest()

    repetitions, elapsed, _ = timed_test(hash_data)
    print(f'   {repetitions * 8 / elapsed:,.0f} MiB/second\n', flush=True)
    del data

    print(f'4. Multicore floating point ({WORKERS} processes)...', flush=True)
    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=WORKERS) as executor:
        results = list(executor.map(worker_float, [TEST_SECONDS] * WORKERS))
    elapsed = time.perf_counter() - start
    total_ops = sum(item[0] for item in results)
    multi_rate = total_ops / elapsed
    print(f'   {multi_rate:,.0f} total iterations/second')
    print(f'   Multicore/single-process speedup: {multi_rate / single_rate:.2f}x')
    print(f'   Multicore test elapsed (including startup): {elapsed:.1f} s\n')
    print('Benchmark complete.')


if __name__ == '__main__':
    main()
