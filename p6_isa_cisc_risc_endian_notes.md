# Computer Architecture: ISA, RISC, CISC, Memory Addressing, M1 vs Pi5, Endianness

**AI generated notes - Lehman Fall 2026**

**Learning objectives**

By the end of this lesson, students should be able to:

1. Explain the basic difference between RISC and CISC.
2. Distinguish between instruction size, register size, and memory address size.
3. Explain how instructions reference registers and memory.
4. Describe the difference between 32-bit and 64-bit applications.

---

## 1. RISC vs. CISC: The Big Picture (3 minutes)

Processors use an *Instruction Set Architecture (ISA)*, which defines the machine instructions they understand.

Two important approaches to instruction-set design are:

- **RISC — Reduced Instruction Set Computer:** Emphasizes relatively simple, regular instructions.
- **CISC — Complex Instruction Set Computer:** Supports more varied instructions, including instructions capable of combining multiple operations.

| Feature | RISC | CISC |
|---|---|---|
| Instruction design | Simple, regular | More varied and flexible |
| Instruction length | Often fixed | Often variable |
| Arithmetic | Usually register-to-register | Can involve memory directly |
| Memory access | Separate load/store operations | Some instructions combine operations |
| Examples | ARM64, RISC-V | x86-64 |

**Real-world examples**

- Raspberry Pi 5 — ARM64 (RISC)
- Apple M1 — ARM64 (RISC)
- Intel Core 5 — x86-64 (CISC)

**Important:** RISC does not necessarily mean fewer instructions, fewer operands, or a less sophisticated processor.

Modern x86-64 has roughly 1,000 distinct instruction mnemonics, depending on how they are counted. Modern ARM64 also has a large instruction set.

**Ask students:** Which is RISC: Apple M1 or Intel Core 5?

*Answer: Apple M1.*

---

## 2. Comparing Actual Instructions (4 minutes)

### Adding two numbers

**ARM64 (RISC)**

```asm
add x0, x1, x2
```

Meaning:

```text
X0 = X1 + X2
```

Three operands: destination, source 1, source 2.

**x86-64 (CISC, GNU AT&T syntax)**

```asm
addq %rbx, %rax
```

Meaning:

```text
RAX = RAX + RBX
```

Two operands: source and destination. The destination is also one of the inputs.

**Discussion:** Why does RISC have three operands when CISC has two?

The number of operands does not determine instruction complexity. ARM64 uses a regular format with explicit source and destination registers.

### Adding 5 to a variable in memory

Suppose X0 (ARM64) or RAX (x86-64) contains the memory address of a variable.

**ARM64**

```asm
ldr x1, [x0]
add x1, x1, #5
str x1, [x0]
```

Three instructions:

1. Load the value from memory.
2. Add 5 in a register.
3. Store the result in memory.

**x86-64**

```asm
addq $5, (%rax)
```

One instruction reads the value from memory, adds 5, and writes it back.

This illustrates a fundamental distinction:

**RISC generally separates memory access and arithmetic. CISC can combine them.**

### Can one instruction reference two memory locations?

Yes. The x86 instruction `movsb` copies one byte between the memory addresses held in RSI and RDI.

Ordinary x86 `ADD` instructions, however, cannot have two explicit memory operands.

---

## 3. Instruction Size vs. Register Size (4 minutes)

There are three different concepts:

- **Instruction size:** The number of bits in a machine instruction.
- **Register size:** The number of bits a register can hold.
- **Address size:** The number of bits used to represent a memory address.

| Feature | ARM64 | x86-64 |
|---|---|---|
| Register width | 64 bits | 64 bits |
| Instruction length | Fixed 32 bits | Variable 8–120 bits |
| General-purpose registers | 31 (X0–X30) | 16 traditional 64-bit registers |
| Register identification | 5-bit field | Commonly 3-bit field plus extensions |

### How can a 32-bit instruction reference three 64-bit registers?

ARM64 provides 32 register encodings.

\[
2^5 = 32
\]

Therefore, **only 5 bits are needed to identify one register**.

For example:

```asm
add x0, x1, x2
```

- X0: 5 bits to identify the destination register
- X1: 5 bits to identify the first source register
- X2: 5 bits to identify the second source register

Total: 15 bits to identify the registers.

The remaining 17 bits of the 32-bit instruction specify the operation and other details.

**Important distinction:** The register holds 64 bits of data, but only 5 bits are needed to identify which register to use.

### How does x86-64 support instructions longer than 64 bits?

x86-64 instructions have variable lengths.

Examples:

| Instruction | Size |
|---|---|
| `nop` | 8 bits |
| `ret` | 8 bits |
| `addq %rbx, %rax` | 24 bits |
| `movabsq $0x123456789ABCDEF0, %rax` | 80 bits |

The processor fetches the instruction as a sequence of bytes and decodes the complete instruction.

A 64-bit processor does not mean instructions must be 64 bits long.

**Ask students:** How many bits are needed to identify one of 16 registers?

*Answer: 4 bits.*

---

## 4. How Instructions Access Memory (4 minutes)

A 64-bit processor can use 64-bit addresses even when instructions are only 32 bits long.

### Register-indirect addressing

Suppose:

- Memory address 1000 contains the value 42.
- Register X0 contains 1000.

ARM64:

```asm
ldr x1, [x0]
```

The processor:

1. Reads X0 to obtain the memory address.
2. Accesses that memory location.
3. Loads the value 42 into X1.

The instruction does not need to contain the entire memory address. It only needs to identify X0.

### How does an address get into a register?

A processor can construct a large address using multiple instructions.

For example, ARM64 can construct a 64-bit constant using `MOVZ` and `MOVK`:

```asm
movz x0, #0xDEF0
movk x0, #0x9ABC, lsl #16
movk x0, #0x5678, lsl #32
movk x0, #0x1234, lsl #48
```

Result:

```text
X0 = 0x123456789ABCDEF0
```

These four 32-bit instructions build one 64-bit value.

x86-64 can load that same constant using one 80-bit instruction:

```asm
movabsq $0x123456789ABCDEF0, %rax
```

In practice, programs frequently calculate addresses relative to registers or the program counter, avoiding the need to construct full addresses this way.

### Connection to MARIE

MARIE uses 16-bit instructions with a 12-bit address field.

\[
2^{12}=4096
\]

Its directly addressable memory contains 4,096 words.

Unlike ARM64, MARIE typically places a memory address field directly in the instruction. MARIE also supports indirect addressing, where a memory location contains another address.

**Key point:** Instruction size does not determine the maximum address space of a modern processor.

---

## 5. 32-Bit vs. 64-Bit Applications and Raspberry Pi OS (3 minutes)

A 32-bit address can represent:

\[
2^{32}=4,294,967,296
\]

For byte-addressable memory, this is **4 GiB of address space**.

A 64-bit pointer has a much larger theoretical range:

\[
2^{64} \text{ addresses}
\]

Actual processors and operating systems generally implement less than the full theoretical 64-bit address space.

### Raspberry Pi 5

The Raspberry Pi 5 has a 64-bit ARM processor but supports both 32-bit and 64-bit Raspberry Pi OS userlands.

| Feature | 32-bit OS userland | 64-bit OS userland |
|---|---|---|
| Application pointers | Typically 32 bits | Typically 64 bits |
| Application address space | At most 4 GiB, often less usable | Much larger |
| Supported application instructions | AArch32 | AArch64 |
| Instruction length | 16/32 bits in Thumb-2 | Fixed 32 bits |

On the Pi 5, the kernel can be 64-bit even when applications are 32-bit.

### Demonstration commands

Check the kernel architecture:

```bash
uname -m
```

Check the installed Debian/Raspberry Pi OS userland architecture:

```bash
dpkg --print-architecture
```

Check Python's pointer size:

```bash
python3 -c "import struct; print(struct.calcsize('P') * 8)"
```

Typical results:

- `aarch64` — 64-bit ARM kernel
- `armhf` — 32-bit userland
- `arm64` — 64-bit userland
- Python pointer size — 32 or 64 bits

### Virtual memory

A program using only 100 MB of memory does not necessarily use 27-bit pointers.

The operating system assigns virtual memory regions, which may be spread across a much larger address space. A 64-bit application normally uses 64-bit pointers even when it uses very little actual memory.

RISC versus CISC does not determine the size of an application's virtual memory allocation.

---

## 6. Wrap-Up and Questions (2 minutes)

**Five important takeaways**

1. RISC emphasizes simple, regular instructions; CISC supports more varied instructions.
2. ARM64 uses fixed 32-bit instructions; x86-64 uses variable-length instructions.
3. The number of operands does not determine whether an instruction is RISC or CISC.
4. Instructions can reference 64-bit registers and memory addresses without containing all 64 bits themselves.
5. Application pointer size, register width, instruction size, and memory size are different concepts.

### Quick questions for students

**Q1.** Why can ARM64 use three registers in one 32-bit instruction?

*Each register can be identified using only 5 bits.*

**Q2.** Does a 64-bit processor require 64-bit instructions?

*No. Apple M1 and Raspberry Pi 5 use 32-bit AArch64 instructions.*

**Q3.** What is one major difference between ARM64 and x86-64 memory operations?

*ARM64 generally separates loads/stores from arithmetic, while x86-64 can combine memory access and arithmetic.*

**Q4.** Can an application using 100 MB of memory still have 64-bit pointers?

*Yes. The pointer size is determined by the application architecture, not by the amount of memory allocated.*

**Q5.** If Apple M1 and Raspberry Pi 5 use the same ARM64 instruction set, why do they have different performance?

*They implement the same basic ISA using different microarchitectures, including different execution units, caches, and pipelines.*

---

**Final thought**

An instruction set architecture defines **what instructions a processor understands**. The microarchitecture determines **how the processor implements and executes those instructions**.

RISC and CISC describe instruction-set design approaches, not the overall sophistication or performance of a processor.


---
# Follow-Up Questions and Clarifications

1. **So, I used to tell students that 64 bit CPUs process 64 bits at a time, 32 bit CPU's 32 bits at a time, but that is not accurate.**

Correct. Your original explanation was a reasonable simplification, but saying that a 64-bit CPU processes 64 bits at a time is misleading.

A more accurate explanation is:

> A 64-bit processor has general-purpose registers that are 64 bits wide and can perform arithmetic on 64-bit integers using its native instruction set. However, it can also process smaller or larger amounts of data, depending on the instruction and hardware.

## What does 64-bit actually mean?

There are several different widths within a processor:

| Component                 | Intel Core 5 (x86-64)         | Apple M1 (ARM64)          |
| ------------------------- | ----------------------------- | ------------------------- |
| General-purpose registers | 64 bits                       | 64 bits                   |
| Integer arithmetic        | 8, 16, 32, 64 bits            | Commonly 32, 64 bits      |
| Instruction size          | 8–120 bits                    | Fixed 32 bits             |
| SIMD/vector registers     | Up to 256 bits on many models | 128-bit SIMD              |
| Memory addresses          | Typically 64-bit pointers     | Typically 64-bit pointers |
| Memory transfers          | Various sizes                 | Various sizes             |

Notice that both processors can operate on 128-bit vectors even though they are called 64-bit processors.

## An example: A 64-bit processor working on different amounts of data

An x86-64 processor can execute:

```
addb %bl, %al       # Add two 8-bit values
addw %bx, %ax       # Add two 16-bit values
addl %ebx, %eax     # Add two 32-bit values
addq %rbx, %rax     # Add two 64-bit values
```

All four instructions run on the same 64-bit processor!

With SIMD instructions, it can perform operations on multiple numbers simultaneously using even wider registers.

## What about memory transfers?

A 64-bit processor doesn't necessarily read exactly 64 bits from memory at a time.

For example, it might:

- Load a single byte.
- Load an 8-byte integer.
- Load a 16-byte vector.
- Transfer a 64-byte cache line (512 bits) between levels of the memory hierarchy.

The amount transferred depends on the operation and memory subsystem.

## How I would update your classroom explanation

I would tell students:

> Historically, we often described a 32-bit processor as processing 32 bits at a time and a 64-bit processor as processing 64 bits at a time.
>
> That captures the idea of the processor's natural integer data size, but modern processors are much more flexible.
>
> A 64-bit CPU has 64-bit general-purpose registers and native 64-bit integer operations. It can also operate on smaller values and use wider vector instructions.
>
> The 64-bit designation does not tell us how many bits every instruction contains or how many bits the processor fetches from memory at once.

One additional distinction worth teaching: A 64-bit processor is not necessarily twice as fast as a 32-bit processor. The designation describes architectural capabilities, not performance.

I think this is a particularly useful refinement to your lesson: 32-bit versus 64-bit primarily describes the processor's general-purpose register and native integer capabilities, not the amount of data it processes in every operation.

2. **Why is m1 so much faster than raspberry pi 5?**

The Apple M1 is substantially faster than the Raspberry Pi 5 not because it uses a different instruction set, but because its internal CPU design is much more sophisticated.

Both processors use ARM64 (RISC), both have 64-bit registers, and both execute 32-bit instructions.

This makes them excellent examples for teaching the difference between instruction set architecture (ISA) and microarchitecture.

## 1. How much faster is the M1?

Here are representative Geekbench 6 CPU benchmark results.

Geekbench 6 CPU performance

Higher is better. Representative benchmark results.

Apple M1

Raspberry Pi 5

02.5K5K7.5K10KSingle-coreMulti-core

Single-core performance

# 3.1×

M1 faster

Multi-core performance

# 5.3×

M1 faster

These figures are drawn from published Geekbench 6 results for the M1 Mac mini and Raspberry Pi 5. They are illustrative rather than controlled, same-environment tests.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.raspberrypi.com\&sz=32)

Raspberry Pi+1



## 2. Why is the M1 faster?

| Feature                 | Apple M1                                | Raspberry Pi 5 |
| ----------------------- | --------------------------------------- | -------------- |
| Instruction set         | ARM64                                   | ARM64          |
| CPU cores               | 4 performance + 4 efficiency            | 4 Cortex-A76   |
| Clock speed             | Approximately 3.2 GHz performance cores | 2.4 GHz        |
| CPU microarchitecture   | Apple-designed Firestorm and Icestorm   | ARM Cortex-A76 |
| Manufacturing process   | 5 nm                                    | 16 nm          |
| Memory bandwidth        | About 68 GB/s                           | Up to 17 GB/s  |
| Shared/high-level cache | Larger cache resources                  | 2 MB shared L3 |


There are four major reasons for the performance difference.

First, the M1 can do more work per clock cycle. Apple's performance cores have wider instruction execution resources, sophisticated branch prediction, and substantial out-of-order execution capabilities. They can find and execute more independent instructions in parallel.

Second, the M1 has more CPU cores. Its four performance cores and four efficiency cores provide more total processing capacity than the Pi's four Cortex-A76 cores.

Third, the M1 has a much faster memory system. Larger caches and approximately four times the theoretical memory bandwidth help keep its CPU cores supplied with data.

Fourth, the M1 benefits from a more advanced chip design. Its 5 nm manufacturing process enables a higher transistor density, allowing Apple to devote more hardware to processing, caching, and other functions. The process node alone does not determine speed, but it helps enable the design.


## 3. The most important teaching concept: Instructions per clock

A useful simplified formula is:

\\[ \text{CPU performance}\propto \text{Clock speed}\times\text{Instructions per clock (IPC)} \\]

This describes instruction throughput for a comparable workload, assuming the same amount of work is required.

The M1's performance cores run at approximately 3.2 GHz versus 2.4 GHz for the Pi 5.

That's only a 33% clock-speed advantage.

Yet the M1's single-core benchmark score is approximately three times as high.

The additional performance largely comes from doing more useful work per clock cycle, supported by better branch prediction, larger caches, wider execution resources, and other microarchitectural improvements.

A caution for students: benchmark ratios do not directly measure IPC, because benchmark performance also reflects memory behavior and other factors.

## 4. A useful analogy for class

Imagine two students performing the same set of arithmetic problems.

Both students understand the same mathematical operations (the ARM64 instruction set).

But one student has a faster calculator, can work on multiple independent calculations simultaneously, and has frequently needed information readily available.

The other student performs the same operations but with fewer resources.

The first student completes the work faster, even though both are following the same instructions.

That is essentially the difference between the M1 and Raspberry Pi 5.

## 5. A good classroom question

> If the Apple M1 and Raspberry Pi 5 both execute the same ARM64 instructions, why is the M1 approximately three times faster on single-core benchmarks?

The answer is that the instruction set tells us what operations a processor can perform, but the microarchitecture determines how efficiently it performs them.

This also connects directly to the RISC/CISC discussion. An Intel Core 5, Apple M1, and Raspberry Pi 5 all have different internal designs. The RISC/CISC distinction alone tells us very little about their relative performance.

For your 20-minute lesson, I would make this the concluding point:

ISA = What the processor can do.

Microarchitecture = How the processor does it, and how efficiently.

---
3. **How does endianness fit into this?**

Endianness fits directly into our discussion of memory addressing, register size, and instruction sets. It describes the order in which the bytes of a multi-byte value are stored in memory.

The interesting point is that both ARM64 (RISC) and x86-64 (CISC) typically use little-endian byte ordering. Endianness is not fundamentally a RISC versus CISC distinction.

## 1. Big-endian vs. little-endian

Suppose we have a 32-bit hexadecimal value:

`0x12345678`

This value requires four bytes:

`12` `34` `56` `78`

How are those bytes arranged in memory?

32-bit value: 0x12345678

Increasing memory addresses from left to right

Big-endian — most significant byte first

1000

## 12

1001

## 34

1002

## 56

1003

## 78

Little-endian — least significant byte first

1000

## 78

1001

## 56

1002

## 34

1003

## 12

Both arrangements represent the same 32-bit number. The difference is which byte is stored at the lowest memory address.

## 2. How this relates to ARM64 and x86-64

| Architecture           | Typical byte ordering                                                   |
| ---------------------- | ----------------------------------------------------------------------- |
| Intel Core 5 (x86-64)  | Little-endian                                                           |
| Apple M1 (ARM64)       | Little-endian                                                           |
| Raspberry Pi 5 (ARM64) | Little-endian                                                           |
| RISC-V                 | Little-endian in standard application environments                      |
| MARIE                  | Not meaningfully emphasized in its standard word-addressed memory model |

ARM architectures have historically supported more than one byte ordering, but macOS on Apple Silicon and Raspberry Pi OS use little-endian.

This provides another important teaching point:

Endianness and RISC/CISC are independent architectural characteristics.

## 3. Does endianness affect registers?

Not in the same way.

Suppose the ARM64 register `W0` contains:

`0x12345678`

That register holds a numerical value. Endianness becomes relevant when the processor stores the value into byte-addressable memory.

For example:

```
str w0, [x1]
```

If `X1` contains address 1000, the four bytes will be stored in little-endian order:

| Address | Value |
| ------- | ----- |
| 1000    | `78`  |
| 1001    | `56`  |
| 1002    | `34`  |
| 1003    | `12`  |

When the processor later loads all four bytes as a 32-bit value, it reconstructs `0x12345678`.

## 4. How endianness relates to instruction length

Remember our earlier x86-64 example:

```
movabsq $0x123456789ABCDEF0, %rax
```

The instruction is 10 bytes long:

```
48 B8 F0 DE BC 9A 78 56 34 12
```

The first two bytes identify the instruction. The remaining eight bytes encode the 64-bit constant in little-endian order.

This demonstrates that byte ordering is also relevant when interpreting the multi-byte immediate values contained in machine instructions.

One important qualification: endianness does not mean reversing the entire sequence of instruction bytes. The opcode and other fields follow the encoding rules defined by the instruction set.

## 5. A quick Python classroom demonstration

This works on either your Raspberry Pi or Intel-based Linux server.

```
number = 0x12345678print("Big-endian:")print(number.to_bytes(4, byteorder="big").hex(" "))print("Little-endian:")print(number.to_bytes(4, byteorder="little").hex(" "))
```

Expected output:

```
Big-endian:
12 34 56 78
Little-endian:
78 56 34 12
```

Students can see that the same integer produces two different byte sequences.

In summary ...

> We've been discussing how processors find memory locations and load values into registers. There's one more question: if a value occupies multiple bytes, in what order are those bytes stored?
>
> That's endianness. Big-endian stores the most significant byte at the lowest address; little-endian stores the least significant byte at the lowest address.
>
> Interestingly, our Intel Core 5, Apple M1, and Raspberry Pi 5 all use little-endian ordering, even though Intel is CISC and ARM is RISC.


Final connection: Register width tells us how many bits a register can hold. Memory addressing tells us where the data is located. Endianness tells us how the bytes of that data are arranged in memory.

These are three independent but closely related ideas in computer architecture.

-- end --




