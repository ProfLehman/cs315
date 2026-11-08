
# Sample responses for review questions 8 to 10

8. The hexadecimal value 14253647₁₆ is a 32-bit integer consisting of four bytes: `14`, `25`, `36`, and `47`.

| Address | Little Endian | Big Endian |
| ------- | ------------- | ---------- |
| 100     | 47            | 14         |
| 101     | 36            | 25         |
| 102     | 25            | 36         |
| 103     | 14            | 47         |

Explanation:

- Little Endian: Stores the least significant byte (`47`) at the lowest memory address.
- Big Endian: Stores the most significant byte (`14`) at the lowest memory address.

Both representations store exactly the same integer, `0x14253647`. Only the order of the bytes in memory differs.

---

9. The following implementations compute A = (B - C) \* D without modifying the original values of B, C, or D.

Assume that `A`, `B`, `C`, and `D` are memory locations and that registers and the stack can hold intermediate results.

## 3-Address Machine

Format: `OP destination, source1, source2`

```
SUB R1, B, C       ; R1 = B - C
MUL A, R1, D       ; A = R1 * D
```

## 2-Address Machine

Format: `OP destination, source`

The destination is also the first operand.

```
LOAD R1, B         ; R1 = B
SUB  R1, C         ; R1 = R1 - C
MUL  R1, D         ; R1 = R1 * D
STORE A, R1        ; A = R1
```

## 1-Address Machine

Uses an implicit accumulator (AC).

```
LOAD B             ; AC = B
SUB C              ; AC = AC - C
MUL D              ; AC = AC * D
STORE A            ; A = AC
```

## 0-Address Machine

Uses a stack, with arithmetic instructions operating on the top two stack values.

```
PUSH B             ; Push value of B
PUSH C             ; Push value of C
SUB                ; Pop C and B, push B - C
PUSH D             ; Push value of D
MUL                ; Pop D and (B-C), push result
POP A              ; Store result in A
```

## Comparison

| Machine   | Instructions | Intermediate storage |
| --------- | ------------ | -------------------- |
| 3-address | 2            | Register R1          |
| 2-address | 4            | Register R1          |
| 1-address | 4            | Accumulator          |
| 0-address | 6            | Stack                |

Important assumptions: The 3-address machine permits memory locations as source and destination operands. 
The 2-address machine permits memory operands in arithmetic instructions and uses `LOAD destination, source` 
and `STORE destination, source`. These are conventions for the hypothetical machines, not universal instruction formats.

---

10. Given the instruction `LOAD 400` and register R1 = 200, the answers are:

| Addressing Mode | Value Loaded into AC | Explanation                                                                              |
| --------------- | -------------------- | ---------------------------------------------------------------------------------------- |
| a. Immediate    | 400                  | Load the value 400 directly.                                                             |
| b. Direct       | 200                  | Load the contents of memory address 400.                                                 |
| c. Indirect     | 700                  | Address 400 contains 200. Load the contents of address 200, which is 700.                |
| d. Indexed      | 100                  | Add R1 (200) to 400, giving address 600. Load the contents of address 600, which is 100. |

### Memory reference

| Memory Address | Value Stored |
| -------------- | ------------ |
| 200            | 700          |
| 400            | 200          |
| 500            | 800          |
| 600            | 100          |
| 700            | 900          |

Key distinction:

- Immediate: AC = 400
- Direct: AC = M[400] = 200
- Indirect: AC = M[M[400]] = M[200] = 700
- Indexed: AC = M[400 + R1] = M[600] = 100

Here, `M[x]` represents the value stored at memory address `x`.

-- end --
