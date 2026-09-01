@echo off
setlocal
cd /d "%~dp0"
title Hospital Workflow App

if not exist ".venv\Scripts\python.exe" goto setup
".venv\Scripts\python.exe" -c "import sys" >nul 2>nul
if errorlevel 1 goto rebuild_venv
goto install

:rebuild_venv
echo A Python environment copied from another PC was found.
echo Rebuilding the disposable .venv folder for this PC...
rmdir /s /q ".venv"
if exist ".venv" goto cleanup_error

:setup
echo Creating the Python environment. This may take a few minutes.
where py >nul 2>nul
if not errorlevel 1 goto setup_with_py
where python >nul 2>nul
if errorlevel 1 goto python_error
python -m venv .venv
goto setup_done

:setup_with_py
py -3 -m venv .venv

:setup_done
if errorlevel 1 goto python_error

:install
echo Checking required packages...
".venv\Scripts\python.exe" -m pip install -r requirements.txt --disable-pip-version-check
if errorlevel 1 goto package_error

echo.
echo Host PC: http://localhost:8501
echo Client PCs on the approved LAN: http://HOST-NAME-OR-IP:8501
echo Keep this window open while the app is in use.
".venv\Scripts\python.exe" -m streamlit run app.py --server.address 0.0.0.0 --server.port 8501 --server.headless false
echo The app has stopped.
pause
exit /b 0

:python_error
echo Python setup failed.
echo Install Python 3.11 or later and enable the Python launcher or PATH option.
pause
exit /b 1

:package_error
echo Package installation failed.
echo Check the approved network or offline package source, then try again.
pause
exit /b 1

:cleanup_error
echo The old .venv folder could not be removed.
echo Close programs using it, delete only the .venv folder, and run this file again.
pause
exit /b 1
