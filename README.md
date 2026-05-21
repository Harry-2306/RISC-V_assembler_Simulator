# RISC-V 32-Bit Assembler & Instruction Set Simulator

A comprehensive, lightweight toolchain implemented in Python for converting RISC-V assembly programs into machine-executable binaries and simulating their cycle-by-cycle operational lifecycle.

---

## Architecture Overview

This project consists of two core components designed to mimic a hardware processor's execution pipeline:

1. **The Assembler (`Assembler.py`):** A two-pass translator that parses standard RISC-V assembly language textual instructions, resolves structural label bounds, validates strict register mapping constraints, and outputs raw 32-bit binary strings.
2. **The Simulator (`Simulator.py`):** An execution engine that hosts an internal representation of 32 architectural registers and a target addressable data memory stack. It tracks operational states cycle-by-cycle via an internal Program Counter (PC) and generates detailed cycle traces.

---

## Component Deep Dive

### 1. Assembler Engine (`Assembler.py`)

The assembler maps abstract instruction formats into standard IEEE/RISC-V multi-field operational binaries. It supports cross-track label parsing to translate branch targets into relative offsets.

* **Two-Pass Execution Strategy:** Extracts labels and isolates branch targets on pass one before scaling text blocks into dynamic opcode transformations on pass two.
* **Immediate Vector Formats:** Features dynamic bitwise masking and 2's complement generation to encode immediate integer spans safely inside variable widths (12-bit and 21-bit signed bounds).
* **Virtual Halt Guard:** Enforces valid execution terminations by scanning for a dedicated virtual halt instruction (`00000000000000000000000001100011\n`).

### 2. Instruction Set Simulator (`Simulator.py`)

The simulation engine maintains execution parity with hardware layouts, tracking state registers alongside continuous block segments of the heap/stack.

* **Cycle State Tracing:** Appends explicit architectural tracking rows into output streams following each executed cycle, reporting the PC alongside binary values for all 32 registers.
* **Unsigned Data Wrappers:** Employs modular arithmetic loops to force register boundaries to wrap perfectly inside 32-bit configurations:

$$\text{Value}_{\text{unsigned}} = \text{Value} \pmod{2^{32}}$$

* **Memory Boundary Checkers:** Restricts memory lookup scopes exclusively to valid addressable zones (`0x00010000` through `0x0001007C`), terminating cleanly on out-of-bounds pointer leaks.

---

## Supported Instruction Configurations

| Type | Mnemonics | Machine Layout Map |
|---|---|---|
| **R-Type** | `add`, `sub`, `slt`, `srl`, `or`, `and` | funct7 (7b) \| rs2 (5b) \| rs1 (5b) \| funct3 (3b) \| rd (5b) \| opcode (7b) |
| **I-Type** | `lw`, `addi`, `jalr` | imm[11:0] (12b) \| rs1 (5b) \| funct3 (3b) \| rd (5b) \| opcode (7b) |
| **S-Type** | `sw` | imm[11:5] (7b) \| rs2 (5b) \| rs1 (5b) \| funct3 (3b) \| imm[4:0] (5b) \| opcode (7b) |
| **B-Type** | `beq`, `bne` | imm[12] \| imm[10:5] (6b) \| rs2 (5b) \| rs1 (5b) \| funct3 (3b) \| imm[4:1] (4b) \| imm[11] \| opcode (7b) |
| **J-Type** | `jal` | imm[20] \| imm[10:1] (10b) \| imm[11] \| imm[19:12] (8b) \| rd (5b) \| opcode (7b) |

---

---

## Defensive Error Checking & Invalidation

Both software nodes feature validation wrappers designed to handle syntax errors, malformed assembly configurations, or unsafe hardware behaviors:

* **Token Formatting Invalidation:** Catches missing command delimiters, improperly formatted trailing commas, or misplaced expressions.
* **Register Alias Validations:** Maps and filters register identities against ABI identifiers (`zero`, `ra`, `sp`) and alternate target tags (`x0`-`x31`, `r0`-`r31`).
* **Immediate Bounds Clipping:** Throws errors if immediate integers exceed the available hardware bit widths (e.g., values falling outside the signed 12-bit range of -2048 to 2047 for I-Type instructions).
* **Control Flow Alignment Verification:** Confirms that target branch offsets are clean multiples of 4 bytes, guarding against illegal misaligned instruction pointer faults.
* **Label Namespace Integrity:** Scans for and flags identical labels tracking multiple instruction entry addresses.

---
