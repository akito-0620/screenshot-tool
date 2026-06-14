@echo off
setlocal

cd /d "%~dp0"

if not exist ".venv\Scripts\pythonw.exe" (
  echo Virtual environment was not found.
  echo Please run setup first:
  echo   python -m venv .venv
  echo   .\.venv\Scripts\python.exe -m pip install -r structured_screenshot_tool\requirements.txt
  pause
  exit /b 1
)

if not exist "structured_screenshot_tool\main.py" (
  echo Application file was not found.
  pause
  exit /b 1
)

start "" "%~dp0.venv\Scripts\pythonw.exe" "%~dp0structured_screenshot_tool\main.py"
