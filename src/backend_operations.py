# backend_operations.py
import os
import subprocess
import tempfile

def find_vs_dev_cmd():
    """Finds the path to the Visual Studio 2022 Developer Command Prompt script."""
    possible_paths = [
        r"C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\Tools\VsDevCmd.bat",
        r"C:\Program Files\Microsoft Visual Studio\2022\Professional\Common7\Tools\VsDevCmd.bat",
        r"C:\Program Files\Microsoft Visual Studio\2022\Enterprise\Common7\Tools\VsDevCmd.bat",
        r"C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\Common7\Tools\VsDevCmd.bat"
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

def check_requirements():
    """Checks for VS Tools and OpenCV."""
    yield "--- Starting Requirement Checks ---"
    
    yield "\n[1/2] Checking for Visual Studio C++ Tools..."
    vs_cmd_path = find_vs_dev_cmd()
    if vs_cmd_path:
        yield f"  [SUCCESS] Found VS Tools: {vs_cmd_path}"
    else:
        yield "  [FAILURE] Could not find 'VsDevCmd.bat'. Please install 'Desktop development with C++' for VS 2022."
        yield "--- Checks Failed ---"
        return

    yield "\n[2/2] Checking for OpenCV..."
    opencv_dir = os.getenv('OPENCV_DIR')
    if opencv_dir and os.path.exists(opencv_dir):
        yield f"  [SUCCESS] Found OPENCV_DIR: {opencv_dir}"
    else:
        yield "  [FAILURE] 'OPENCV_DIR' environment variable is not set or invalid."
        yield "--- Checks Failed ---"
        return
        
    yield "\n--- All Requirements Met Successfully! ---"

def run_build_process(project_dir, executable_name, status_queue):
    """Dynamically creates and runs a batch script to build the project."""
    temp_script_path = None
    try:
        vs_cmd_path = find_vs_dev_cmd()
        if not vs_cmd_path:
            status_queue.put("[ERROR] Could not find Visual Studio Developer Command Prompt.")
            return

        status_queue.put(">>> Generating dynamic build script...")

        # MODIFIED SCRIPT: It no longer runs the executable.
        # Instead, it prints a unique success signal for the GUI to catch.
        # MODIFIED SCRIPT: It now uses a "safe" signal without special characters.
        script_content = f"""
        @echo off
        cd /d "{project_dir}"
        if %errorlevel% neq 0 ( echo ERROR: Could not navigate to project directory. & exit /b 1 )

        if not exist "build" ( echo "build" directory not found. Creating it... & mkdir build )
        cd build
        if %errorlevel% neq 0 ( echo ERROR: Failed to create or enter the "build" directory. & exit /b 1 )

        echo Running CMake to configure the project...
        cmake .. -G "NMake Makefiles"
        if %errorlevel% neq 0 ( echo. & echo !!! CMAKE FAILED. !!! & echo. & exit /b 1 )
        echo CMake configuration successful.
        echo.

        echo Running nmake to compile the project...
        nmake
        if %errorlevel% neq 0 ( echo. & echo !!! NMAKE BUILD FAILED. Check C++ code for errors. !!! & echo. & exit /b 1 )
        echo Build successful.
        echo.

        if exist "{executable_name}" (
            echo **************************************************
            echo *   SUCCESS: Executable Found: {executable_name}
            echo **************************************************
            echo.
            echo __BUILD_SUCCESS_SIGNAL__
        ) else (
            echo.
            echo ERROR: BUILD SUCCEEDED, BUT EXECUTABLE NOT FOUND!
            echo       Check the 'add_executable' name in CMakeLists.txt
            echo.
        )
        echo ########## BUILD SCRIPT FINISHED ##########
        """

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.bat', encoding='utf-8') as f:
            f.write(script_content)
            temp_script_path = f.name
        
        status_queue.put("-" * 60)

        full_command = f'call "{vs_cmd_path}" -arch=x64 && call "{temp_script_path}"'
        
        process = subprocess.Popen(
            full_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            shell=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        for line in iter(process.stdout.readline, ''):
            status_queue.put(line.strip())
        
        process.stdout.close()
        process.wait()
        status_queue.put("-" * 60)
        status_queue.put(">>> Build process finished.")

    except Exception as e:
        status_queue.put(f"\n[CRITICAL ERROR] An exception occurred: {e}")
    finally:
        if temp_script_path and os.path.exists(temp_script_path):
            os.remove(temp_script_path)