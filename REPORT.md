# Short Project Report

## Project Title

Local Language Programming for Beginners: An Afaan Oromoo-to-Python Translator

## Objective

The project goal is to design a small and readable programming language for beginners using Afaan Oromoo keywords, then translate that language into valid Python code. The focus is usability and clarity rather than language complexity.

## Design Decisions

Python was chosen as the target language because it is readable, widely taught, and supports Unicode identifiers. This allows generated code to preserve Afaan Oromoo names where appropriate.

The implementation follows a clear compiler front-end architecture:

1. Lexer: Tokenizes source text with Unicode-safe rules
2. Parser: Builds a structured AST from token sequences
3. Translator: Converts AST nodes into valid Python syntax

This architecture ensures the system performs structural translation, not simple string replacement.

The execution workflow was also simplified so the Afaan Oromoo source file can be run directly from the project runner or editor integration. The translator now writes the generated Python file and immediately executes it, which makes the `.yl` file the practical entry point for learners.

The language remains intentionally compact and includes only beginner-essential constructs:

- `haaraa` for variable declaration
- Arithmetic and comparison expressions
- `yoo` and `yookan` for branching
- `yeroo` for looping
- `hojii` and `deebi` for function logic
- `xumur` for explicit block closure
- `maxxansi` for beginner-friendly output

## Beginner-Centered Benefits

The language reduces cognitive load by allowing students to read core programming flow in their local language. This lowers early intimidation and improves comprehension during first exposure to coding.

Two design choices are especially effective for beginners:

1. Explicit block closure with `xumur`
This makes nesting boundaries easy to see without relying only on indentation.

2. Local-language output command with `maxxansi`
Learners can write and read simple programs entirely in Afaan Oromoo-oriented syntax while still generating correct Python output.

In addition, translator errors are reported in Afaan Oromoo with line and column context, supporting faster debugging during learning.

## Challenges and Resolutions

Challenge 1: Unicode tokenization and identifiers

- Risk: Incorrect handling of Afaan Oromoo symbols in variable and function names
- Resolution: Lexer rules use Unicode-aware character checks, enabling stable handling of Afaan Oromoo and Latin identifiers

Challenge 2: Simplicity versus correctness

- Risk: Over-simplifying the language could break required functionality
- Resolution: A small grammar was retained, but all mandatory constructs were fully implemented and tested

Challenge 3: Beginner readability with executable output

- Risk: Friendly syntax might generate invalid code
- Resolution: AST-based translation guarantees syntactically correct Python output while preserving beginner-friendly source design

Challenge 4: Direct run support from VS Code on Windows

- Risk: The editor could pass the `.yl` file to Python incorrectly, causing PowerShell quoting errors
- Resolution: The workspace runner was configured to call the translator with PowerShell-safe quoting so clicking Run can execute `.yl` files directly

## Conclusion

The final system meets assignment constraints and demonstrates that a local-language programming interface can significantly improve beginner accessibility without sacrificing correctness. The project now supports a smoother authoring flow: students can write Afaan Oromoo source programs in `.yl`, run them directly, and receive Python execution results without manually managing the translated file. This provides a practical foundation for inclusive programming education in Ethiopian classrooms.
