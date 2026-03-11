@echo off
cd /d "%~dp0"
title SAFI PROTOCOL DSP ENGINE v5.0 - Omerta Music Research
color 06
echo.
echo  SAFI PROTOCOL DSP ENGINE v5.0
echo  Omerta Music Research - Casablanca - 2026
echo  64-bit Linear Phase Offline Mastering
echo.

where python >nul 2>&1
if errorlevel 1 (
    echo Python non trouve. Telechargement...
    powershell -Command "Start-Process 'https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe' -Wait"
    echo Relancer SAFI.bat apres installation.
    pause & exit
)

python -c "import numpy,scipy" >nul 2>&1
if errorlevel 1 (
    echo Installation des dependances...
    python -m pip install --quiet numpy scipy
)

set PYTHONIOENCODING=utf-8
python "%~dp0safi_app_v5.py"
if errorlevel 1 pause
