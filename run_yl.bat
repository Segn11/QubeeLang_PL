@echo off
setlocal

if "%~1"=="" (
    echo Usage: run_yl.bat ^<program.yl^>
    exit /b 1
)

set "SOURCE=%~1"

if not exist "%SOURCE%" (
    echo File not found: %SOURCE%
    exit /b 1
)

if /I not "%~x1"==".yl" (
    echo Input must be a .yl file
    exit /b 1
)

set "PYTHON_EXE=%~dp0.venv\Scripts\python.exe"
if exist "%PYTHON_EXE%" (
    "%PYTHON_EXE%" "%~dp0translator.py" "%SOURCE%"
) else (
    python "%~dp0translator.py" "%SOURCE%"
)
if errorlevel 1 exit /b 1

endlocal
