@echo off
REM Change to the project directory (adjust the path as needed)
cd "C:\Users\TJ\Documents\Code\ISU Match History"

REM Activate the virtual environment
call .\venv\Scripts\activate

REM Clear the Streamlit cache
streamlit cache clear

REM Start the Streamlit app
streamlit run app.py

REM Pause to keep the window open and display any errors
pause
