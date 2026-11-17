
# performance_2026.py
# CS315 Computer Architecture
# Prof. Lehman - Developed with ChatGPT fall 2026
# File Writing Performance Benchmark
#
# Tests different write block sizes while keeping the total file size fixed.
# Python's file buffering is disabled. The OS is asked to synchronize
# the completed file once per run (not after each block).

import os
import time


def write_file(filename, total_size, block_size):
    """Write total_size bytes using block_size writes; return elapsed seconds."""
    data = b'A' * block_size
    bytes_written = 0

    start = time.perf_counter()

    with open(filename, 'wb', buffering=0) as f:
        while bytes_written < total_size:
            amount = min(block_size, total_size - bytes_written)

            # Unbuffered raw-file writes can technically be partial.
            written = f.write(data[:amount])
            if written is None or written <= 0:
                raise OSError('File write failed')
            bytes_written += written

        # Request that the OS synchronize data to the storage device.
        os.fsync(f.fileno())

    return time.perf_counter() - start


def main():
        
    size_kb = int(input("Enter total file size in KB (e.g., 1000): "))
    total_size = size_kb * 1000

    if total_size <= 0:
        print('File size must be greater than zero.')
        return

    block_sizes = [256, 512, 1024, 2048, 4096, 8192]
    
    repetitions = 3
    

    # ***************************************************************************
    # *** Adjust output from SSD to USB here ************************************
    # ***************************************************************************
    # For USB testing, change this to a path on the USB drive, such as:
    
    # Windows example
    # filename = r'D:\benchmark.dat'  
    
    # Mac OS example
    # filename = '/Volumes/MY_USB/benchmark.dat'
    
    # write to harddrive (ie. SSD or mechanical hard drive) 
    filename = 'benchmark.dat'

    # ***************************************************************************
    
    
    print('\nFile Writing Performance Benchmark')
    print(f'Total file size: {size_kb:,} KB ({total_size:,} bytes)')
    print(f'Runs per block size: {repetitions}\n')
    print(f"{'Block (bytes)':>14} {'Write calls':>14} {'Avg time (s)':>15} {'MB/s':>12}")
    print('-' * 59)

    try:
        for block_size in block_sizes:
            times = []

            for _ in range(repetitions):
                times.append(write_file(filename, total_size, block_size))

            avg_time = sum(times) / repetitions
            write_calls = (total_size + block_size - 1) // block_size
            #throughput = (total_size / (1024 * 1024)) / avg_time    # MiB per second
            throughput = (total_size / 1_000_000) / avg_time         # MB per second

            print(f'{block_size:>14,} {write_calls:>14,} '
                  f'{avg_time:>15.4f} {throughput:>12.2f}')
                        

    finally:
        # Remove the file created by the benchmark.
        if os.path.exists(filename):
            os.remove(filename)


if __name__ == '__main__':
    main()
