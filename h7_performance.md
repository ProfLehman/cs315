



### 4. File Writing Performance Benchmark

Run the sample Python program [performance_2026.py](performance_2026.py) on your personal computer. The program measures how different write block sizes affect file-writing performance.

**a.** Review the program, which writes data using block sizes of 256, 512, 1024, 2048, 4096, and 8192 bytes. Each test runs three times and reports the average execution time and transfer rate (MB/s).

**b.** Select three different file sizes (in KB) that produce meaningful performance results. Choose sizes that allow the tests to complete in a reasonable amount of time. Run the benchmark for each file size using your computer's internal storage.

**c.** Create a table and graph showing your results for the three file sizes. The graph should compare write block size (horizontal axis) with average execution time (vertical axis), using a separate series for each file size. Write a paragraph interpreting your results. How does block size affect performance? Did larger blocks always produce faster results? Were the results what you expected?

### **Sample Table – Part C: File Writing Performance**

**Average execution time (seconds) by block size and total file size**

| Block Size (bytes) | 4,000 KB (4 MB) | 8,000 KB (8 MB) | 16,000 KB (16 MB) |
| ------------------ | --------------- | --------------- | ----------------- |
| 256                | 0.1417          | 0.2811          | 0.5571            |
| 512                | 0.0740          | 0.1495          | 0.3176            |
| 1,024              | 0.0444          | 0.0860          | 0.1739            |
| 2,048              | 0.0274          | 0.0537          | 0.1130            |
| 4,096              | 0.0205          | 0.0358          | 0.0725            |
| 8,192              | 0.0096          | 0.0234          | 0.0421            |

Sample results from an internal SSD. Each value represents the average of three benchmark runs. Lower times indicate better performance.

### **Sample Graph – Part C: File Writing Performance**
![Sample Graph PartC](partc_graph.png)



**d.** Select a USB storage device and determine its advertised or expected write transfer rate (MB/s). USB drives are available to borrow if needed. Modify the program's output filename to write directly to the USB drive. Run the benchmark using one of the same file sizes from part (b).

Create a table comparing the performance of your USB drive and internal storage for each block size. Write a paragraph comparing their performance and discussing how the measured USB transfer rate compares with its advertised or expected performance. Explain possible reasons for any unexpected results, considering the operating system, filesystem, and storage hardware.

**Submit:** Your benchmark results, table(s), graph, and two paragraphs interpreting your findings.



