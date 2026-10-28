# Lab: Python, MARIE, and Native Assembly

**40 points**  
**Due date:** Friday, November 6

## Objective

Compare three ways of executing the same program: MARIE's **accumulator**, Python's **stack-based bytecode**, and a real processor's **register-based assembly language**. You may use AI to generate and debug code, but you must test the programs and understand how they work.

## Assigned numbers

Use your assigned value of `N` in **all four** Python programs and translations.

| Student | Name | N |
|---|---|---:|
| Student A | __________________ | 3 |
| Student B | __________________ | 5 |
| Student C | __________________ | 7 |
| Student D | __________________ | 9 |
| Student E | __________________ | 11 |
| Student F | __________________ | 13 |

## The four Python programs

Replace `7` with your assigned number. Include your **name** in a comment at the top of each source file. Keep the algorithms intact in every translation; do not simply print the expected answer.

### Program 1 — Arithmetic

```python
# Your name
N = 7
x = N + 10
y = N * 2
z = (x + y) * 2
print(z)
```

### Program 2 — Conditional

```python
# Your name
N = 7
x = N * 3
y = 40 - N

if x > y:
    z = x
else:
    z = y

print(z)
```

### Program 3 — Loop

```python
# Your name
N = 7
total = 0
i = 1

while i <= N:
    total = total + i
    i = i + 1

print(total)
```

### Program 4 — Array

```python
# Your name
N = 7
numbers = [N, N + 5, N + 10, N + 15]
total = 0

for value in numbers:
    total = total + value

print(total)
```

The translated versions of Program 3 must execute a **real loop**. The translated versions of Program 4 must actually traverse an array stored in memory (using indirect or indexed addressing), not replace it with four separate constant additions.

## Files to create

Create **three items for each program**, using the following names:

| File | Purpose |
|---|---|
| `p1.py` | Original customized Python source |
| `p1.dis` | Readable Python bytecode listing produced by `dis` |
| `p1.s` | Native x86-64 or ARM64 assembly source |

Repeat for `p2`, `p3`, and `p4`. The `.dis` file is **text**, not an executable bytecode file. Python's compiled `.pyc` files are a different format. The standard extension for GNU assembly source is **`.s`**, not `.a` (`.a` often indicates an archive/library).

### 1. Python and bytecode

Run the Python program and then create its readable bytecode listing:

```bash
python p1.py
python -m dis p1.py > p1.dis
```

Repeat with `p2.py`, `p3.py`, and `p4.py`. Use `python --version` to check your Python version. Take a screenshot showing each Python program executing and its **numerical output**. Keep the `.py` and `.dis` files available for grading.

### 2. MARIE

Use the online simulator at **https://marie.js.org/** to create and test a MARIE version of **each** program. Do not use an `ORG` statement; let the program start at address `000`. Use the simulator's **Get share URL** command to generate a link for each completed program. Open each link yourself to verify that it contains the correct code. Include the four links in your submission, labeled `P1` through `P4`. The instructor will open and run them.

### 3. x86-64 or ARM64 assembly

Choose **one platform for all four programs**:

- **x86-64 on Ada:** Write `p1.s` through `p4.s` in your Ada account. Leave your source files, executables, and screenshots in a clearly named assignment directory in your account. The instructor will inspect them using authorized administration access; do not submit passwords.
- **ARM64 on Raspberry Pi (optional):** Rather than using Ada, write and run the same four `.s` programs on the Pi. Save your source files, executables, and screenshots on the assigned SD card, and physically submit that **clearly labeled SD card**. Ensure the card is shut down and removed safely.

On a Linux target with GCC installed, example commands are:

```bash
gcc -g p1.s -o p1
./p1
objdump -d p1
```

Repeat for all programs. Take a screenshot showing the execution command and correct numerical output for **each** assembly program. Keep the source and screenshots together for grading. Your native assembly must match your target processor (`x86_64` on Ada or `aarch64` on a 64-bit Raspberry Pi); check with `uname -m`.

## What to submit

**In the assignment submission**, provide:

1. **Four MARIE share links** (`P1`–`P4`).
2. **Answers to the five questions below** (about 2–4 sentences per question).
3. **Your selected native platform** (Ada x86-64 or Raspberry Pi ARM64) and, for Ada, the directory location where your files can be found.

**Leave on Ada or submit on the Raspberry Pi SD card:**

- `p1.py`–`p4.py` (4 Python programs).
- `p1.dis`–`p4.dis` (4 readable bytecode listings).
- `p1.s`–`p4.s` (4 native assembly source files), the corresponding executables, and screenshots showing successful execution/output of Python and native assembly for each program.

The instructor will verify the MARIE programs through the shared links. If a shared link fails, you may be asked to provide the MARIE source directly.

## Five questions (answer once, after completing all programs)

Answer each of the following questions (1 or 2 paragraphs each).

1. **Accumulator vs. stack:** How does MARIE's accumulator differ from the operand stack used by Python bytecode? Use Program 1 as an example.
2. **Registers:** How does your chosen native architecture (x86-64 or ARM64) perform arithmetic differently from MARIE and Python bytecode? Include one actual assembly instruction from your code.
3. **Control flow:** Which instructions implement the conditional in Program 2 and the loop in Program 3? Give an example from MARIE and one from your native assembly.
4. **Memory addressing:** How does Program 4 access the array elements in MARIE compared with your native assembly program?
5. **AI verification:** Describe one issue you corrected in AI-generated code **or** one significant claim you independently checked. How did you verify correctness?

## Grading (40 points)

| Component | Points |
|---|---:|
| Four MARIE programs and working share links (4 × 3) | 12 |
| Four Python programs, bytecode listings, and execution screenshots (4 × 2) | 8 |
| Four native assembly programs and execution screenshots (4 × 3) | 12 |
| Five written questions (5 × 1.6) | 8 |
| **Total** | **40** |

**Important:** The code must implement the requested computations, branches, loops, and memory accesses. Merely producing the correct answer with a hard-coded constant is not sufficient. AI assistance is permitted and encouraged (required, unless you already know how to write assembler), but you are responsible for testing every program.
