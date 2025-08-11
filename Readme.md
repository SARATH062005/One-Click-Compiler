# C++ OpenCV Build Tool

This application provides a user-friendly graphical interface to compile and run C++ projects that use OpenCV, specifically configured for the Visual Studio 2022 environment on Windows.

## Prerequisites

1.  **Python:** You must have Python installed. You can download it from [python.org](https://www.python.org/downloads/). During installation, make sure to check the box that says **"Add Python to PATH"**.

2.  **Visual Studio 2022:** You need the **"Desktop development with C++"** workload installed. This provides the necessary MSVC compiler, headers, and the "x64 Native Tools Command Prompt" environment.

3.  **OpenCV:** You must have OpenCV downloaded and configured with the `OPENCV_DIR` environment variable pointing to your OpenCV build folder (e.g., `C:\opencv\build`).

## Installation

Once the prerequisites are met, you need to install one Python library for the user interface.

1.  Open a Command Prompt or PowerShell window.
2.  Run the following command to install `customtkinter`:

    ```sh
    pip install customtkinter
    ```

## How to Run the Application

1.  Place all the project files (`main.py`, `backend_operations.py`) in the same folder.
2.  Open a command prompt in that folder.
3.  Run the main application file with the following command:

    ```sh
    python main.py
    ```

The application window should now appear.