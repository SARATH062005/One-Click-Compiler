# main.py
import tkinter
import customtkinter as ctk
from tkinter import filedialog
import threading
import queue
import os  # <-- THIS LINE WAS MISSING
from backend_operations import check_requirements, run_build_process

# Set appearance and color theme
ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Configuration ---
        self.title("C++ OpenCV Build Tool")
        self.geometry("800x600")

        # --- State Variables ---
        self.is_building = False
        self.status_queue = queue.Queue()

        # --- Layout Configuration ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # --- Widgets ---
        
        # Frame for Path Entry
        self.path_frame = ctk.CTkFrame(self)
        self.path_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.path_frame.grid_columnconfigure(1, weight=1)

        self.path_label = ctk.CTkLabel(self.path_frame, text="Project Path:")
        self.path_label.grid(row=0, column=0, padx=10, pady=10)

        self.path_entry = ctk.CTkEntry(self.path_frame, placeholder_text="Enter the path to your C++ code folder")
        self.path_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.browse_button = ctk.CTkButton(self.path_frame, text="Browse...", command=self.browse_path)
        self.browse_button.grid(row=0, column=2, padx=10, pady=10)

        # Frame for Main Buttons
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(row=1, column=0, padx=10, pady=0, sticky="ew")
        self.button_frame.grid_columnconfigure((0,1,2), weight=1)
        
        self.check_button = ctk.CTkButton(self.button_frame, text="Check Requirements", command=self.run_checks)
        self.check_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.build_button = ctk.CTkButton(self.button_frame, text="Compile and Run", command=self.start_build)
        self.build_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.exit_button = ctk.CTkButton(self.button_frame, text="Exit", command=self.quit, fg_color="#D32F2F", hover_color="#B71C1C")
        self.exit_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        # Terminal Output Box
        self.terminal = ctk.CTkTextbox(self, font=("Consolas", 12))
        self.terminal.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.terminal.configure(state="disabled")

        # Start processing the queue for status updates
        self.process_queue()

    def browse_path(self):
        """Opens a dialog to select a directory and inserts it into the path entry."""
        path = filedialog.askdirectory(title="Select Project Folder")
        if path:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, path)

    def update_terminal(self, message):
        """Inserts a message into the terminal box and scrolls to the end."""
        self.terminal.configure(state="normal")
        self.terminal.insert("end", message + "\n")
        self.terminal.see("end")
        self.terminal.configure(state="disabled")

    def run_checks(self):
        """Runs the requirement checks from the backend."""
        self.terminal.configure(state="normal")
        self.terminal.delete("1.0", "end")
        self.terminal.configure(state="disabled")
        for message in check_requirements():
            self.update_terminal(message)

    def start_build(self):
        """Starts the build process in a new thread to avoid freezing the GUI."""
        if self.is_building:
            self.update_terminal("[INFO] A build is already in progress.")
            return
            
        project_path = self.path_entry.get()
        if not project_path:
            self.update_terminal("[ERROR] Please provide a project path first.")
            return

        self.is_building = True
        self.build_button.configure(state="disabled", text="Building...")
        self.check_button.configure(state="disabled")
        
        self.terminal.configure(state="normal")
        self.terminal.delete("1.0", "end")
        self.terminal.configure(state="disabled")
        
        # Assumption: executable name is the folder name. This line now works.
        executable_name = os.path.basename(project_path) + ".exe"

        # Run the build process in a separate thread
        build_thread = threading.Thread(
            target=run_build_process,
            args=(project_path, executable_name, self.status_queue),
            daemon=True
        )
        build_thread.start()

    def process_queue(self):
        """
        Checks the queue for new messages from the worker thread and updates the GUI.
        Reschedules itself to run again after 100ms.
        """
        try:
            while not self.status_queue.empty():
                message = self.status_queue.get_nowait()
                self.update_terminal(message)
                
                # Check for end-of-process signals
                if ">>> Process finished" in message or "[ERROR]" in message or "[CRITICAL ERROR]" in message or "BUILD FAILED" in message:
                    self.is_building = False
                    self.build_button.configure(state="normal", text="Compile and Run")
                    self.check_button.configure(state="normal")

        except queue.Empty:
            pass
        finally:
            self.after(100, self.process_queue)

if __name__ == "__main__":
    app = App()
    app.mainloop()