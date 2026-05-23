# Required Test Programs

This document provides the required three test programs with source code, generated target code, and execution output.

## 1. Basic Program (Variables + Math)

### Source (`tests/program1_basic_math.yl`)

```yl
# Program 1: Variables and math (Afaan Oromoo keywords)
haaraa x = 8
haaraa y = 4
haaraa z = x + y * 2
maxxansi("Bu'aa z:", z)
```

### Generated Target (`tests/program1_basic_math.py`)

```python
# Auto-generated from .yl (Afaan Oromoo language)
x = 8
y = 4
z = (x + (y * 2))
print("Bu'aa z:", z)
```

### Execution Result

```text
Bu'aa z: 16
```

## 2. Control Flow Program

### Source (`tests/program2_control_flow.yl`)

```yl
# Program 2: if/else and while (Afaan Oromoo keywords)
haaraa n = 5
haaraa total = 0

yeroo n > 0:
    total = total + n
    n = n - 1
xumur

yoo total > 10:
    maxxansi("Waliigala guddaa:", total)
yookan:
    maxxansi("Waliigala xiqqaa:", total)
xumur
```

### Generated Target (`tests/program2_control_flow.py`)

```python
# Auto-generated from .yl (Afaan Oromoo language)
n = 5
total = 0
while (n > 0):
    total = (total + n)
    n = (n - 1)
if (total > 10):
    print('Waliigala guddaa:', total)
else:
    print('Waliigala xiqqaa:', total)
```

### Execution Result

```text
Waliigala guddaa: 15
```

## 3. Feature Demonstration (Functions)

### Source (`tests/program3_functions_feature.yl`)

```yl
# Program 3: Functions and return (Afaan Oromoo keywords)
hojii multiply_by_four(x):
    deebi x * 4
xumur

haaraa result = multiply_by_four(6)
maxxansi("Bu'aa =", result)
```

### Generated Target (`tests/program3_functions_feature.py`)

```python
# Auto-generated from .yl (Afaan Oromoo language)
def multiply_by_four(x):
    return (x * 4)
result = multiply_by_four(6)
print("Bu'aa =", result)
```

### Execution Result

```text
Bu'aa = 24
```
