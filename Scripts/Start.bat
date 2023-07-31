@REM Start the python script

@echo off
@REM Ensure that python is installed
python --version > NUL 2>&1
if errorlevel 1 (
    echo Python is not installed
    echo Please install python and try again
    pause
    exit
)

@REM Ensure that the required python modules are installed
python -c "import pyside6" > NUL 2>&1
if errorlevel 1 (
    echo PYSide6 is not installed
    echo Please install PYSide6 and try again
    pause
    exit
)

python "main.py"

