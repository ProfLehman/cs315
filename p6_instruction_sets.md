# Lab: From Python to Machine Architecture

**Course:** Computer Organization / Architecture  
**Due Date:** [To be announced]  
**Student Name:** ____________________

## Overview

In MARIE, you learned how an accumulator-based computer executes instructions. In this lab, you will compare that architecture with Python's stack-based virtual machine and a modern register-based processor.

You will use AI to assist with translating four Python programs into MARIE assembly and either x86-64 or ARM64 assembly. You must test the generated code, identify the important instructions, and explain how each architecture executes the same algorithm.

## Learning Objectives

After completing this lab, you should be able to:

1. Explain the differences between accumulator, stack, and register-based architectures.
2. Examine actual Python bytecode using the `dis` module.
3. Translate Python programs into MARIE assembly.
4. Translate Python programs into x86-64 or ARM64 assembly.
5. Assemble and execute programs on a real processor.
6. Explain how different architectures handle arithmetic, branching, loops, and memory.
7. Evaluate and correct AI-generated assembly code.

## Assigned Student Numbers

Each student must use their assigned number, **N**, in all four programs.

| Student | Name | Assigned Number (N) |
|---|---|---|
| Student 1 | __________ | 3 |
| Student 2 | __________ | 5 |
| Student 3 | __________ | 7 |
| Student 4 | __________ | 9 |
| Student 5 | __________ | 11 |
| Student 6 | __________ | 13 |

Replace the example value `N = 7` with your assigned number in each program.

## Architecture Requirements

All students must complete the following for each of the four programs:

1. Run the original Python program.
2. Examine and explain its Python bytecode.
3. Translate the program into MARIE assembly and execute it.
4. Translate the program into **one** of the following architectures:
   - **x86-64 assembly** running on the Ada Linux server.
   - **ARM64 assembly** running on a Raspberry Pi (optional).
5. Execute the assembly program and verify that its output matches Python.

Use the same native architecture for all four programs.

---

## Program 1: Arithmetic

**Concepts:** Arithmetic operations, intermediate values, accumulator, operand stack, and registers.

```python
# your name
N = 7  # Replace with your assigned number

x = N + 10
y = N * 2
z = (x + y) * 2

print(z)
```

### Questions

1. How does MARIE perform the addition?
2. How does Python's operand stack handle `x + y`?
3. Where does the x86-64 or ARM64 processor store the intermediate result?
4. How is multiplication by 2 implemented in your MARIE program?

---

## Program 2: Conditional Branching

**Concepts:** Comparisons, conditional instructions, and branching.

```python
# your name
N = 7  # Replace with your assigned number

x = N * 3
y = 40 - N

if x > y:
    z = x
else:
    z = y

print(z)
```

### Questions

1. How does MARIE determine which branch to execute?
2. Which Python bytecode instructions implement the comparison and branch?
3. Which instructions perform the comparison and branch in x86-64 or ARM64?
4. What happens to the program counter when a branch is taken?

**Additional requirement:** Test both possible branches by temporarily changing N. Record the additional test value and its result.

---

## Program 3: Loops

**Concepts:** Loop counters, conditional branches, and program control.

```python
# your name
N = 7  # Replace with your assigned number

total = 0
i = 1

while i <= N:
    total = total + i
    i = i + 1

print(total)
```

### Questions

1. How does MARIE implement the loop?
2. Which Python bytecode instruction causes execution to jump backward?
3. How does the x86-64 or ARM64 version implement repetition?
4. Where is the loop counter stored in each architecture?

**Requirement:** Your MARIE and native assembly programs must contain actual loops. Do not substitute the mathematical formula for the result.

---

## Program 4: Arrays and Memory Addressing

**Concepts:** Arrays, memory locations, pointers, indirect addressing, and load/store instructions.

```python
N = 7  # Replace with your assigned number

numbers = [N, N + 5, N + 10, N + 15]

total = 0

for value in numbers:
    total = total + value

print(total)
```

### Questions

1. How are the four array elements stored in MARIE memory?
2. How does MARIE's `LoadI` instruction work?
3. Which Python bytecode instructions implement iteration through the list?
4. How are array elements accessed in x86-64 or ARM64?
5. What is the difference between direct and indirect memory addressing?

**Requirement:** Your MARIE and native assembly programs must store four values in consecutive memory locations and traverse them. Do not replace the loop with four hard-coded additions.

---

# Part 1: Examine Python Bytecode

For each program:

1. Save the customized Python code as `program1.py`, `program2.py`, and so forth.
2. Run the program and record its output.
3. Display the bytecode using:

```bash
python -m dis program1.py
```

4. Record your Python version:

```bash
python --version
```

5. Copy the bytecode listing into your submission.
6. Identify and explain at least four important bytecode instructions.
7. Show how the operand stack changes during an important calculation or operation.

**Note:** Python bytecode instructions can vary between Python versions. Use the instructions generated by your installed version.

# Part 2: Translate into MARIE

For each program:

1. Ask AI to translate your Python code into MARIE assembly.
2. Review the generated instructions.
3. Assemble and execute the program in the MARIE simulator.
4. Correct any errors.
5. Verify that its output matches the original Python program.

Your programs must preserve the original algorithms, including conditional branches, loops, and array traversal.

Submit the MARIE source code and evidence of successful execution.

# Part 3: Translate into x86-64 or ARM64

Choose one architecture:

- **Option A:** x86-64 on Ada.
- **Option B:** ARM64 on a Raspberry Pi.

For each program:

1. Ask AI to generate complete Linux-compatible assembly source.
2. Save the program as a `.s` file.
3. Assemble and link the program using GCC.
4. Execute the program.
5. Verify the output.
6. Examine part of the resulting machine code.

Example commands:

```bash
gcc -g program1.s -o program1
./program1
objdump -d program1
```

Your generated assembly must match the architecture of the computer executing it.

# Part 4: Comparing Architectures

Complete the following table for your selected native architecture.

| Feature | MARIE | Python Bytecode | x86-64 or ARM64 |
|---|---|---|---|
| Primary operand storage | | | |
| Number of explicit arithmetic operands | | | |
| How addition is performed | | | |
| How conditional branches work | | | |
| How loops are implemented | | | |
| How memory is accessed | | | |
| Where intermediate results are stored | | | |

Then answer:

1. What are the advantages and disadvantages of an accumulator-based architecture?
2. How does a stack-based architecture differ from a register-based architecture?
3. What is the difference between two-address and three-address instructions?
4. Why are CISC and RISC not defined solely by the number of operands?
5. Which architecture did you find easiest to understand, and why?

# Part 5: Using Artificial Intelligence

You are **encouraged to use AI** to help generate, explain, and debug assembly-language programs.

However, you are responsible for ensuring that every generated program is correct.

### Suggested AI Prompt

> I am studying computer organization and instruction set architectures. Translate the following Python program into MARIE assembly using instructions supported by the MARIE simulator. Preserve the original algorithm, including loops, comparisons, and memory accesses. Do not replace calculations with precomputed answers. Explain each important instruction.
>
> [Paste your Python program here.]

For your native assembly translation, change the prompt to request either x86-64 GNU assembly for Linux or AArch64 GNU assembly for Linux.

For each program, document at least one AI-generated detail that you independently verified or corrected.

# Submission Requirements

Submit the following:

- [ ] Four Python programs with your assigned number.
- [ ] Python bytecode listings for all four programs.
- [ ] Explanations of important stack operations.
- [ ] Four MARIE assembly programs.
- [ ] Evidence that the MARIE programs execute correctly.
- [ ] Four x86-64 or ARM64 assembly programs.
- [ ] Evidence that the native assembly programs execute correctly.
- [ ] Completed architecture comparison table.
- [ ] Answers to the comparison questions.
- [ ] Documentation of AI assistance and your verification work.

**Important:** Simply producing the correct numerical answer is insufficient. Your programs must implement the required arithmetic, branching, loops, and memory accesses.

# Grading Rubric

| Component | Points |
|---|---:|
| Python bytecode analysis (4 × 5) | 20 |
| MARIE implementations (4 × 8) | 32 |
| x86-64 or ARM64 implementations (4 × 8) | 32 |
| Architecture comparison and questions | 10 |
| AI verification and documentation | 6 |
| **Total** | **100** |
