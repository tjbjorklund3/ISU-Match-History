@echo off
REM Change to the project directory
cd /d "C:\Users\TJ\Documents\Code\ISU Match History"

REM Check if the virtual environment folder exists
if not exist ".\.venv\Scripts\activate.bat" (
    echo Virtual environment not found. Please ensure the .venv exists in this folder.
    echo Create one with: python -m venv .venv
    pause
    exit /b
)

REM Activate the virtual environment
call ".\.venv\Scripts\activate.bat"

REM Ensure Streamlit is installed in the virtual environment
if not exist ".\.venv\Scripts\streamlit.exe" (
    echo Streamlit is not installed in the virtual environment.
    echo Run: pip install streamlit
    pause
    exit /b
)

REM Clear Streamlit cache and run the app
.\.venv\Scripts\streamlit.exe cache clear
.\.venv\Scripts\streamlit.exe run app.py

REM Pause the script to prevent it from closing automatically
pause
