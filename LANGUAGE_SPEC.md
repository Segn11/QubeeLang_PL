# Afaan Oromoo Beginner Programming Language Specification

## 1. Overview

This document defines a small programming language for beginners using Afaan Oromoo keywords. The language is intentionally minimal and readable. It is translated into Python through a structured lexer-parser-translator pipeline.

Language goals:

- Reduce beginner confusion by using familiar local language keywords
- Keep syntax small and consistent
- Preserve enough core features for basic programming tasks
- Generate correct, readable Python output

File extension:

- Source file: `.yl`
- Generated file: `.py`

## 2. Core Design Philosophy

The language focuses on clarity rather than advanced features.

Beginner-friendly design choices:

- Keywords are in Afaan Oromoo
-- Blocks are explicit with `xumur` instead of relying only on indentation
- Error messages are in Afaan Oromoo
- Syntax is line-oriented and predictable

Why this helps beginners:

- Students can read control flow in familiar words
-- Explicit block ending (`xumur`) makes nested structures easier to see
- Clear parser errors in local language reduce intimidation

## 3. Lexical Rules (Unicode-Aware)

The lexer supports Unicode identifiers. This means variable and function names can be written in Afaan Oromoo or Latin.

### 3.1 Identifiers

Identifier start characters:

- Any Unicode alphabetic character (`isalpha`) or `_`

Identifier continuation characters:

- Unicode alphabetic character, digit, or `_`

Examples:

- `x`
- `maqaa`
- `lakkoofsa`

### 3.2 Literals

Supported literals:

- Integer numbers (`0`, `1`, `42`)
- Strings using single or double quotes

### 3.3 Comments and Whitespace

- Line comments begin with `#`
- Newlines separate statements
- Spaces/tabs are allowed for readability

## 4. Keywords

| Keyword | Meaning |
|---|---|
| `haaraa` | Declare a new variable |
| `yoo` | Start if condition |
| `yookan` | Else branch |
| `yeroo` | While loop |
| `hojii` | Function definition |
| `deebi` | Return value |
| `xumur` | End a block |
| `maxxansi` | Output text/value (maps to Python `print`) |

## 5. Syntax Rules

### 5.1 Variables

Declaration and assignment:

```yl
haaraa x = 10
x = x + 2
```

### 5.2 Expressions

Supported operators:

- Arithmetic: `+`, `-`, `*`, `/`
- Comparison: `==`, `<`, `>`

Precedence (high to low):

1. `*`, `/`
2. `+`, `-`
3. `==`, `<`, `>`

### 5.3 Conditional

```yl
yoo x > 5:
    maxxansi("Caalaa 5")
yookan:
    maxxansi("5 yookan gadi")
xumur
```

### 5.4 Loop

```yl
haaraa n = 3
yeroo n > 0:
    maxxansi(n)
    n = n - 1
xumur
```

### 5.5 Functions

Definition, call, and return:

```yl
hojii dhibe(a, b):
    deebi a + b
xumur

haaraa r = dhibe(2, 3)
maxxansi(r)
```

### 5.6 Built-in Calls

Any identifier followed by `(...)` is parsed as a function call. The language provides the Afaan Oromoo output alias `maxxansi(...)`, which is translated to Python `print(...)`.

## 6. Informal Grammar

```text
program      -> statement* EOF
statement    -> "haaraa" IDENT "=" expression
             | IDENT "=" expression
             | "yoo" expression ":" NEWLINE block ("yookan" ":" NEWLINE block)? "xumur"
             | "yeroo" expression ":" NEWLINE block "xumur"
             | "hojii" IDENT "(" params? ")" ":" NEWLINE block "xumur"
             | "deebi" expression
             | expression

block        -> statement*
params       -> IDENT ("," IDENT)*
expression   -> comparison
comparison   -> term (("==" | "<" | ">") term)*
term         -> factor (("+" | "-") factor)*
factor       -> unary (("*" | "/") unary)*
unary        -> "-" unary | primary
primary      -> NUMBER | STRING | IDENT call? | "(" expression ")"
call         -> "(" arguments? ")"
arguments    -> expression ("," expression)*
```

## 7. Translation to Python

Each parsed AST node is converted to Python syntax:

- Variable declaration and assignment both become `name = expr`
-- `yoo` becomes `if`
-- `yookan` becomes `else`
-- `yeroo` becomes `while`
-- `hojii` becomes `def`
-- `deebi` becomes `return`
- Function calls remain function calls

Generated Python conventions:

- 4-space indentation
- Parenthesized binary expressions for readability
- File header comment for traceability

## 8. Error Handling

The translator reports syntax and lexical errors in Afaan Oromoo with line and column information.

Examples of messages:

- Unknown symbol
- Missing `:` after control-flow headers
-- Missing `xumur` to close a block
- Incomplete string literal

This is a key beginner-support feature.

## 9. Example End-to-End Program

Source (`.yl`):

```yl
hojii kuusaa(x):
    deebi x * 2
xumur

haaraa y = kuusaa(7)
maxxansi(y)
```

Generated Python (`.py`):

```python
def kuusaa(x):
    return (x * 2)

y = kuusaa(7)
print(y)
```

## 10. Scope and Limits

Included:

- Variables
- Integer math and comparison
- If/else
- While loop
- Function define/call/return

Not included (by design):

- Classes
- Lists/dictionaries syntax extensions
- Type system
- VM/bytecode/optimization

The language is intentionally small and focused to meet educational goals.
