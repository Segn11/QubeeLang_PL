# Local Language Programming for Beginners

This project presents a beginner-focused programming language that uses Afaan Oromoo keywords and translates source programs into executable Python code.

## Project Summary

- Language style: Afaan Oromoo-based educational syntax
- Translator type: Source-to-source compiler
- Input file: .yl
- Output file: .py
- Target language: Python

## Key Features

- Variables: declaration and assignment
- Expressions: +, -, *, /, ==, <, >
- Control flow: if/else and while
- Functions: definition, call, return
- Unicode support for Afaan Oromoo identifiers
- Beginner-friendly diagnostics in Afaan Oromoo
- Afaan Oromoo output keyword `maxxansi(...)` mapped to Python print(...)

## Repository Structure

- translator.py: Lexer, parser, AST, and Python code generator
- run_yl.bat: One-command runner for .yl files on Windows
- LANGUAGE_SPEC.md: Complete language specification
- TEST_RESULTS.md: Required test programs and execution results
- REPORT.md: Design report
- tests/: Assignment test programs (.yl and generated .py)

## How To Write Code

1. Create a .yl file, for example x.yl.
2. Write your program using Afaan Oromoo keywords.
3. Save the file with UTF-8 encoding.

Example source program:

```text
haaraa x = 5
haaraa y = 2
maxxansi(x + y)
```

## How To Run Code (Recommended)

Use the one-command runner from the project root:

```powershell
.\run_yl.bat x.yl
```

What this does:

1. Translates x.yl into x.py.
2. Executes the generated Python immediately.

## How To Run Code (Manual)

If you want to inspect the generated Python and then run it yourself:

```powershell
c:/Users/USER/Desktop/pl_prj/.venv/Scripts/python.exe translator.py x.yl
c:/Users/USER/Desktop/pl_prj/.venv/Scripts/python.exe x.py
```

## Requirements

- Python 3.8 or later
- Save `.yl` files using UTF-8 encoding
- Optional: create and activate a virtual environment for running `translator.py`

## Example Assignment Runs

```powershell
.\run_yl.bat tests/program1_basic_math.yl
.\run_yl.bat tests/program2_control_flow.yl
.\run_yl.bat tests/program3_functions_feature.yl
```

## Constraint Compliance

- Unicode-aware lexer: completed
- Structured parser with AST: completed
- No pure text replacement: completed
- Required language constructs: completed
- Valid executable Python output: completed

  ## group members
  
