@echo off
setlocal

echo ##################################################################
echo #           DEVELOPMENT ENVIRONMENT PRE-FLIGHT CHECK             #
echo ##################################################################
echo.
echo This script will check if your system is ready for C++ and
echo OpenCV development with Visual Studio 2022.
echo.

REM --- CHECK 1: Visual Studio C++ Build Tools ---

echo ------------------------------------------------------------------
echo [CHECK 1 of 2] ==> Checking for Visual Studio 2022 C++ Build Tools...
echo ------------------------------------------------------------------
echo.

set "VS_COMMUNITY_VARS_PATH=C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"
set "VS_PROFESSIONAL_VARS_PATH=C:\Program Files\Microsoft Visual Studio\2022\Professional\VC\Auxiliary\Build\vcvars64.bat"
set "VS_ENTERPRISE_VARS_PATH=C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Auxiliary\Build\vcvars64.bat"
set "VS_BUILDTOOLS_VARS_PATH=C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"

set "VS_TOOLS_FOUND=0"
if exist "%VS_COMMUNITY_VARS_PATH%" set "VS_TOOLS_FOUND=1"
if exist "%VS_PROFESSIONAL_VARS_PATH%" set "VS_TOOLS_FOUND=1"
if exist "%VS_ENTERPRISE_VARS_PATH%" set "VS_TOOLS_FOUND=1"
if exist "%VS_BUILDTOOLS_VARS_PATH%" set "VS_TOOLS_FOUND=1"

REM This is the corrected IF statement using quotes for robustness.
if "%VS_TOOLS_FOUND%"=="1" (
    echo  [SUCCESS] Visual Studio C++ Build Tools ^(x64^) are installed.
) else (
    echo  [FAILURE] Could not find the x64 Native Tools for Visual Studio 2022.
    echo.
    echo  To fix this, you need to install the required components from the
    echo  Visual Studio Installer.
    echo.
    echo  --- HOW TO INSTALL ---
    echo.
    echo  1. Open the Start Menu and search for "Visual Studio Installer".
    echo  2. Find your installation of Visual Studio 2022 and click "Modify".
    echo     ^(If you don't have Visual Studio, you can download the "Build Tools"^)
    echo     from the Visual Studio website^).
    echo.
    echo  3. Go to the "Workloads" tab.
    echo  4. Check the box for "Desktop development with C++".
    echo  5. On the right-hand side, under "Installation details", make sure that
    echo     the latest "MSVC v143 ... x64/x86 build tools" is selected.
    echo  6. Click the "Modify" or "Install" button on the bottom right.
    echo.
    echo  For more details, visit:
    echo  https://learn.microsoft.com/en-us/cpp/build/vscpp-step-0-installation
)
echo.

REM --- CHECK 2: OpenCV Installation ---

echo ------------------------------------------------------------------
echo [CHECK 2 of 2] ==> Checking for OpenCV...
echo ------------------------------------------------------------------
echo.

if defined OPENCV_DIR (
    if exist "%OPENCV_DIR%\build\x64" (
        echo  [SUCCESS] OpenCV environment variable ^(OPENCV_DIR^) is set to:
        echo            "%OPENCV_DIR%"
        echo            The directory structure appears to be correct.
    ) else (
        echo  [WARNING] OpenCV environment variable ^(OPENCV_DIR^) is set to:
        echo            "%OPENCV_DIR%"
        echo            However, the path does not seem to be a valid OpenCV
        echo            build folder. Please ensure it points to the root
        echo            of your extracted OpenCV directory ^(e.g., C:\opencv^).
    )
) else (
    echo  [FAILURE] The OPENCV_DIR environment variable is not set.
    echo.
    echo  This variable is required for CMake to find your OpenCV installation.
    echo.
    echo  --- HOW TO INSTALL AND CONFIGURE ---
    echo.
    echo  1. Download the latest pre-built OpenCV for Windows from the official site.
    echo     Go to: https://opencv.org/releases/
    echo     Click the "Windows" button for the latest version.
    echo.
    echo  2. Run the downloaded .exe file. It is a self-extracting archive.
    echo     When it asks for a location, extract it to a simple path,
    echo     for example: C:\
    echo     This will create a folder named "opencv" ^(e.g., C:\opencv^).
    echo.
    echo  3. Set the OPENCV_DIR Environment Variable:
    echo     a. Press the Windows key and search for "Edit the system environment variables".
    echo     b. In the window that opens, click the "Environment Variables..." button.
    echo     c. In the "User variables" section at the top, click "New...".
    echo     d. For "Variable name:", enter  OPENCV_DIR
    echo     e. For "Variable value:", enter the path to your opencv build folder,
    echo        which is typically inside your extracted folder.
    echo        For example: C:\opencv\build
    echo     f. Click OK on all windows to save the changes.
    echo.
    echo  4. IMPORTANT: You must RESTART any open command prompts for this change
    echo     to take effect. It is best to restart your computer.
)
echo.

echo ------------------------------------------------------------------
echo Check complete. Please review any FAILURE or WARNING messages above.
echo ------------------------------------------------------------------
echo.
pause
endlocal