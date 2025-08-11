@echo off
setlocal

REM --- START OF USER CONFIGURATION ---

REM 1. Set the full path to your C++ project folder (the one containing CMakeLists.txt)
set "PROJECT_DIR=D:\Test_demo"

REM 2. Set the name of your final executable file (must match the name from CMakeLists.txt)
set "EXECUTABLE_NAME=HoleDiameterDetection.exe"

REM 3. Set the full path to your Visual Studio 2022 VsDevCmd.bat
set "VS_DEV_CMD_PATH=C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\Tools\VsDevCmd.bat"

REM --- END OF USER CONFIGURATION ---


REM --- SCRIPT LOGIC (DO NOT MODIFY BELOW) ---

if not exist "%VS_DEV_CMD_PATH%" (
    echo. & echo ERROR: Visual Studio command prompt not found at: & echo "%VS_DEV_CMD_PATH%" & echo Please correct the path. & echo. & pause & goto :eof
)

call "%VS_DEV_CMD_PATH%" -arch=x64 -host_arch=x64

echo ##################################################################
echo #                 STARTING C++ BUILD SCRIPT                      #
echo ##################################################################
echo.

cd /d "%PROJECT_DIR%"
if %errorlevel% neq 0 ( echo ERROR: Could not navigate to project directory: "%PROJECT_DIR%" & pause & goto :eof )

echo Current Directory: %cd%
echo.

if exist "build" (
    echo "build" directory found. Removing for a clean build...
    rmdir /s /q build
)
echo.

echo Creating "build" directory...
mkdir build
cd build
if %errorlevel% neq 0 ( echo ERROR: Failed to create or enter the "build" directory. & pause & goto :eof )
echo.

echo Running CMake to configure the project...
cmake .. -G "NMake Makefiles"
if %errorlevel% neq 0 (
    echo. & echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! & echo !!!                  CMAKE FAILED.                             !!! & echo !!! Check the error messages above.                            !!! & echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! & echo. & pause & goto :eof
)
echo CMake configuration successful.
echo.

echo Running nmake to compile the project...
nmake
if %errorlevel% neq 0 (
    echo. & echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! & echo !!!                  NMAKE BUILD FAILED.                       !!! & echo !!! This is likely a C++ code error. Review errors above.      !!! & echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! & echo. & pause & goto :eof
)
echo Build successful.
echo.

REM --- Check for executable and ask for permission to run ---
if exist "%EXECUTABLE_NAME%" (
    echo.
    echo **************************************************
    echo *   Executable Found: %EXECUTABLE_NAME%
    echo **************************************************
    echo.
    echo The script is ready to run the compiled program.
    echo.
	
    REM --- THIS IS THE PERMISSION STEP ---
    pause
	
    echo.
    echo Starting application...
    echo --------------------------------------------------
    %EXECUTABLE_NAME%
    echo --------------------------------------------------
) else (
    echo.
    echo ERROR: Build Succeeded, but executable "%EXECUTABLE_NAME%" was not found!
    echo       Check the 'add_executable' name in your CMakeLists.txt and the 'EXECUTABLE_NAME' variable in this script.
    echo.
    pause
)

echo.
echo ##################################################################
echo #                  BUILD SCRIPT FINISHED                         #
echo ##################################################################
echo.
pause
endlocal