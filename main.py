# main.py
import tkinter
import customtkinter as ctk
from tkinter import filedialog
import threading
import queue
import os
import subprocess
import signal
from src.backend_operations import check_requirements, run_build_process

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ONE-CLICK-COMPILER")
        self.geometry("800x600")

        # --- State Variables ---
        self.is_building = False
        self.status_queue = queue.Queue()
        self.executable_path = None
        self.running_process = None

        # --- Layout Configuration ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1) # New row for run controls

        # --- Widgets ---
        # Path Entry Frame
        self.path_frame = ctk.CTkFrame(self)
        self.path_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")
        self.path_frame.grid_columnconfigure(1, weight=1)
        self.path_label = ctk.CTkLabel(self.path_frame, text="Project Path:")
        self.path_label.grid(row=0, column=0, padx=10, pady=5)
        self.path_entry = ctk.CTkEntry(self.path_frame, placeholder_text="Enter path to your C++ code folder")
        self.path_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.browse_button = ctk.CTkButton(self.path_frame, text="Browse...", command=self.browse_path, width=100)
        self.browse_button.grid(row=0, column=2, padx=10, pady=5)

        # Executable Name Frame
        self.exe_frame = ctk.CTkFrame(self)
        self.exe_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        self.exe_frame.grid_columnconfigure(1, weight=1)
        self.exe_label = ctk.CTkLabel(self.exe_frame, text="Executable Name:")
        self.exe_label.grid(row=0, column=0, padx=10, pady=5)
        self.exe_entry = ctk.CTkEntry(self.exe_frame, placeholder_text="e.g., HoleDiameterDetection.exe (Must match CMakeLists.txt)")
        self.exe_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

        # Main Buttons Frame
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        self.button_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.check_button = ctk.CTkButton(self.button_frame, text="Check Requirements", command=self.run_checks)
        self.check_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.build_button = ctk.CTkButton(self.button_frame, text="Build Application", fg_color="#00695C", hover_color="#004D40")
        self.build_button.configure(command=self.start_build)
        self.build_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.exit_button = ctk.CTkButton(self.button_frame, text="Exit", command=self.quit, fg_color="#D32F2F", hover_color="#B71C1C")
        self.exit_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        # --- Run Control Frame (Initially Hidden) ---
        self.run_control_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.run_control_frame.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
        self.run_control_frame.grid_columnconfigure((0,1), weight=1)
        self.run_button = ctk.CTkButton(self.run_control_frame, text="Run Application", command=self.start_executable)
        self.run_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.stop_button = ctk.CTkButton(self.run_control_frame, text="Stop Application", command=self.stop_executable, fg_color="#D32F2F", hover_color="#E65100")
        self.stop_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.run_control_frame.grid_remove() # Hide this frame initially

        # Terminal Output Box
        self.terminal = ctk.CTkTextbox(self, font=("Consolas", 12))
        self.terminal.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
        self.terminal.configure(state="disabled")

        self.process_queue()

    def browse_path(self):
        path = filedialog.askdirectory(title="Select Project Folder")
        if path:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, path)

    def update_terminal(self, message):
        self.terminal.configure(state="normal")
        self.terminal.insert("end", message + "\n")
        self.terminal.see("end")
        self.terminal.configure(state="disabled")

    def run_checks(self):
        self.terminal.configure(state="normal")
        self.terminal.delete("1.0", "end")
        self.terminal.configure(state="disabled")
        for message in check_requirements():
            self.update_terminal(message)

    def start_build(self):
        if self.is_building: return
        self.stop_executable() # Stop any running process before building
        self.run_control_frame.grid_remove() # Hide run controls on new build
        self.executable_path = None

        project_path = self.path_entry.get()
        executable_name = self.exe_entry.get()
        if not all([project_path, executable_name]):
            self.update_terminal("[ERROR] Project Path and Executable Name are required.")
            return

        self.is_building = True
        self.build_button.configure(state="disabled", text="Building...")
        self.check_button.configure(state="disabled")
        self.terminal.configure(state="normal"); self.terminal.delete("1.0", "end"); self.terminal.configure(state="disabled")
        
        threading.Thread(target=run_build_process, args=(project_path, executable_name, self.status_queue), daemon=True).start()

    def start_executable(self):
        if self.running_process:
            self.update_terminal("\n[INFO] Application is already running.")
            return
        if not self.executable_path:
            self.update_terminal("\n[ERROR] No executable path is set. Build the project first.")
            return
        
        self.update_terminal("\n--- Starting Application ---")
        self.run_button.configure(state="disabled")
        self.stop_button.configure(state="normal")

        threading.Thread(target=self._execute_and_stream_output, daemon=True).start()

    def _execute_and_stream_output(self):
        """Helper method to run in a thread and stream process output."""
        try:
            self.running_process = subprocess.Popen(
                [self.executable_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',       # Tell Python to use the universal UTF-8 encoding
                errors='ignore',        # If a byte is still invalid, just discard it instead of crashing
                # shell=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            for line in iter(self.running_process.stdout.readline, ''):
                self.status_queue.put(line.strip())
            
            self.running_process.stdout.close()
            self.running_process.wait()
        except Exception as e:
            self.status_queue.put(f"[ERROR] Failed to run executable: {e}")
        finally:
            self.status_queue.put("--- Application Finished ---")
            self.running_process = None

    def stop_executable(self):
        if self.running_process:
            self.update_terminal("\n--- Stopping Application ---")

            # Try to terminate the process tree on Windows using taskkill
            try:
                # /F: force kill, /T: terminate process tree, /PID: process id
                subprocess.run(["taskkill", "/F", "/T", "/PID", str(self.running_process.pid)],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as e:
                self.update_terminal(f"[ERROR] Failed to stop process tree: {e}")

            self.running_process = None
            self.run_button.configure(state="normal")
            self.stop_button.configure(state="disabled")

    def process_queue(self):
        try:
            while not self.status_queue.empty():
                message = self.status_queue.get_nowait()
                self.update_terminal(message)
                
                # MODIFIED LINE: Look for the new "safe" signal.
                if "__BUILD_SUCCESS_SIGNAL__" in message:
                    self.executable_path = os.path.join(self.path_entry.get(), "build", self.exe_entry.get())
                    self.run_control_frame.grid() # Show the run/stop buttons
                    self.run_button.configure(state="normal")
                    self.stop_button.configure(state="disabled")
                
                if "Build process finished." in message or "NMAKE BUILD FAILED" in message or "CMAKE FAILED" in message:
                    self.is_building = False
                    self.build_button.configure(state="normal", text="Build Application")
                    self.check_button.configure(state="normal")
                
                if "--- Application Finished ---" in message:
                    self.run_button.configure(state="normal")
                    self.stop_button.configure(state="disabled")
        except queue.Empty:
            pass
        finally:
            self.after(100, self.process_queue)

if __name__ == "__main__":
    app = App()
    app.mainloop()