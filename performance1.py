import os
import time
import random
import string

# performance1.py
# fall 2024
# CS315 Lehman
# Code generated via ChatGPT 4o, modified to input KB rather than bytes
# ie. 1 KB = 1024 bytes
#     1,024 KB = 1 MB

"""
File Writing Performance Comparison Program

This program demonstrates the efficiency differences between two file-writing methods:
1. Writing one byte at a time, reopening and closing the file for each byte.
2. Writing data in larger chunks (4 KB per write).

Features:
- The user specifies the maximum file size to write (in bytes).
- The program times the execution of each writing method.
- Results are displayed to show the time taken by each method and highlight the performance difference.

How it works:
1. Byte-by-byte Method:
   - Each byte is written individually, with the file being reopened and closed for every byte.
   - This method incurs significant overhead due to frequent system calls and lack of buffering.

2. Chunked Method:
   - Data is written in chunks of 4 KB (or the remaining size if less than 4 KB).
   - This method is more efficient, leveraging system and disk optimization for block-based writes.

Timing:
- The program uses Python's `time` module to measure the duration of each method.
- Results are printed, showing the time taken for both methods.

Expected Outcome:
- The chunked method is expected to be significantly faster due to reduced system calls,
  better utilization of buffering, and alignment with disk I/O optimizations.

Usage:
1. Run the script and enter the maximum file size (in bytes) when prompted.
2. Observe the time taken for both methods and the comparison results.

Note:
This program is designed for educational purposes to illustrate the importance of choosing efficient
file-writing strategies in software development.

"""

# function writes to file one byte at a time
def write_byte_by_byte(filename, max_size):
    start_time = time.time()
    size_written = 0
    while size_written < max_size:
        with open(filename, "ab") as f:  # Open in append-binary mode
            byte = random.choice(string.ascii_letters).encode()  # Generate one random byte
            f.write(byte)
        size_written += 1
    elapsed_time = time.time() - start_time
    return elapsed_time

# function writes to file using "chucks" of data
def write_in_chunks(filename, max_size, chunk_size=4096):
    start_time = time.time()
    size_written = 0
    with open(filename, "wb") as f:  # Open in write-binary mode
        while size_written < max_size:
            remaining = max_size - size_written
            chunk = ''.join(random.choices(string.ascii_letters, k=min(chunk_size, remaining))).encode()
            f.write(chunk)
            size_written += len(chunk)
    elapsed_time = time.time() - start_time
    return elapsed_time



# *** main **    
max_size = int(input("Enter the maximum file size to write (in KB): "))
max_size = max_size * 1024

byte_by_byte_file = "byte_by_byte.txt"
chunk_file = "chunk_write.txt"
#chunk_file = "e:\chunk_write.txt"   #select alternate drive location


# *** one byte at a time ***
# Ensure old files are removed
if os.path.exists(byte_by_byte_file):
    os.remove(byte_by_byte_file)
    
print("Writing byte by byte...")
byte_time = write_byte_by_byte(byte_by_byte_file, max_size)
#byte_time = 0
print(f"Byte-by-byte write completed in {byte_time:.2f} seconds.")


# *** write 1KB "chunks" ***

# Ensure old files are removed
if os.path.exists(chunk_file):
    os.remove(chunk_file)
    
print("\nWriting in 1 KB chunks...")
chunk_time_1k = write_in_chunks(chunk_file, max_size, 1024)
print(f"Chunked write completed in {chunk_time_1k:.2f} seconds.")


# *** write 4KB "chunks" ***

# Ensure old files are removed
if os.path.exists(chunk_file):
    os.remove(chunk_file)
    
print("\nWriting in 4 KB chunks...")
chunk_time_4k = write_in_chunks(chunk_file, max_size, 4096)
print(f"Chunked write completed in {chunk_time_4k:.2f} seconds.")


# *** Summary ***
print("\nSummary:")
print(f"Byte-by-byte write time: {byte_time:.2f} seconds")
print(f"Chunked 1k write time: {chunk_time_1k:.2f} seconds")
print(f"Chunked 4k write time: {chunk_time_4k:.2f} seconds")
