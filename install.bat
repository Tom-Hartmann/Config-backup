@echo off
cls

echo This script will perform the following actions:
echo.
echo 1. Install Node.js
echo 2. Install Python
echo 3. Install necessary Python libraries
echo 4. Install PM2
echo 5. Launch the Python script using PM2
echo 6. Set the Python script to auto-start using PM2
echo.
echo IMPORTANT: You need to have administrative privileges to run this script.
echo.
set /p "user_input=Do you want to continue with these installations? (yes/no): "
if /i "%user_input%" neq "yes" (
    echo Exiting the installation.
    exit /b
)

:: Check if script has administrative privileges
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\systemprofile" || (
    echo Requesting administrative privileges...
    goto UACPrompt
) || (echo Running with admin privileges, continuing... && goto SkipUAC)

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    exit /B

:SkipUAC

echo Starting installation...

REM 1. Install Node.js
echo Installing Node.js...
bitsadmin /transfer "JobName" https://nodejs.org/dist/v14.17.1/node-v14.17.1-x64.msi %cd%\node_installer.msi
msiexec /i %cd%\node_installer.msi /passive
del node_installer.msi

REM 2. Install Python
echo Installing Python...
bitsadmin /transfer "JobName" https://www.python.org/ftp/python/3.9.5/python-3.9.5-amd64.exe %cd%\python_installer.exe
python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
del python_installer.exe

REM 3. Install necessary Python libraries
echo Installing Python libraries...
python -m pip install --upgrade pip
pip install watchdog configparser

REM 4. Install PM2
echo Installing PM2...
npm install pm2@latest -g

REM 5. Launch Python script using PM2
echo Starting Python script with PM2...
pm2 start backup_monitor.py --name "backup_monitor" --interpreter python

REM 6. Set the Python script to auto-start using PM2
echo Setting script to auto-start with PM2...
pm2 save
pm2 startup

echo Installation and setup complete!
pause
