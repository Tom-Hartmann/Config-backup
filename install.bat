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
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\systemprofile"
if '%errorlevel%' == '0' (
    echo Running with admin privileges, continuing...
    goto SkipUAC
) else (
    echo Requesting administrative privileges...
    goto UACPrompt
)

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    exit /B

:SkipUAC

echo Starting installation...

:: Your installation steps...

echo Installation and setup complete!

:: Ask user if they want to create a bat file in autostart
set /p "autostart_input=Do you want to create a bat file for auto-start? (yes/no): "
if /i "%autostart_input%"=="yes" (
    echo Creating autostart bat file...
    echo @echo off > "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\autostart_pm2.bat"
    echo start "" /B pm2 resurrect >> "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\autostart_pm2.bat"
    echo Autostart bat file created successfully!
) else (
    echo Skipping autostart bat file creation.
)

pause
