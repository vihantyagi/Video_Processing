# video_processor_gui.py

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import cv2
from threading import Thread 

class GUI:

    def __init__(self) -> None:
        self.entry_path = None
        self.entry_fps = None
        self.entry_width = None
        self.entry_height = None
        self.speed_var = None
        self.start_time = None
        self.label_duration = None
        self.final_processing = None
        self.callback = None 
        self.fps, self.frame, self.duration = 0, 0, 0
        self.spinner_label = None 
        self.spinner_symbols = ["|", "/", "-"]  # Spinner characters
        self.running = False

    # Function to select a .mp4 video file
    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")], title="Select a video file")
        if file_path:
            self.entry_path.delete(0, tk.END)
            self.entry_path.insert(0, file_path)
            self.fetch_details()

    def fetch_value(self, Field, entry, data_type=int, type="stats"):
        try:
            if self.on_validate(entry, type):
                value = entry.get()
                if value == "no change":
                    value1 = -1
                else:
                    value1 = data_type(value)
                    if value1 <= 0: 
                        messagebox.showwarning("Warning", f"Please enter positive value for {Field}.")
                        return "reset_value"
                return value1
            else:
                return -1
        except ValueError:
            messagebox.showwarning("Warning", f"Please enter correct data type for {Field}.")
            return "reset_value"
    
    def start_task(self, button_clicked):

        # Validate that video path is an MP4 file
        if not self.entry_path.get().endswith(".mp4"):
            messagebox.showwarning("Warning", "Please select an MP4 file.")
            return
        
        self.start_spinner()
        task_thread = Thread(target=self.process_video, args= ("process",))
        task_thread.start()
        
    # Function to process video with FFmpeg
    def process_video(self, button_pressed="test"):

        video_path = self.entry_path.get()
        speed = self.speed_var.get()

        if (fps := self.fetch_value("FPS", self.entry_fps, int, "stats")) == "reset_value": return
        if (width := self.fetch_value("Width", self.entry_width, int, "stats")) == "reset_value": return
        if (height := self.fetch_value("Height", self.entry_height, int, "stats")) == "reset_value": return
        # if (speed := self.fetch_value("Speed", self.speed_var, float, "stats")) == "reset_value": return
        if (start_time := self.fetch_value("Start Time", self.start_time, int, "start_time")) == "reset_value": return
        if (label_duration := self.fetch_value("Video duration", self.label_duration, int, "label_duration")) == "reset_value": return

        if fps == -1 and width == -1 and height == -1 and speed == -1 and start_time == -1 and label_duration == -1 and button_pressed=="process": 
            text = f"Since no parameter is being changed the software will simply perform standard compression"
            messagebox.showinfo("Please Note", text)

        print(video_path, start_time, label_duration, fps, width, height, speed)
        self.final_processing = (video_path, start_time, label_duration, fps, width, height, speed)

        if self.callback:
            a = self.callback(self.final_processing)
        if a: 
            messagebox.showinfo("Info", "Video processing is complete!")
            self.running = False
            self.spinner_label.config(text="😴")

    def set_callback(self, callback):
        # Allows the main script to set a callback function
        self.callback = callback
    
    # Fetch metadata of the video to be processed. 
    def fetch_details(self):
        
        print(self.entry_path.get())
        cap = cv2.VideoCapture(self.entry_path.get())
        ret, frame = cap.read()
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT) 
        self.fps = cap.get(cv2.CAP_PROP_FPS)

        self.duration = round(frame_count / self.fps) 
        self.frame = frame.shape

    # Function to display information in a popup window
    def get_info(self):

        info_text = f"resolution {self.frame[0]}x{self.frame[1]} \nfps: {int(self.fps)} \nduration: {self.duration} seconds"
        messagebox.showinfo("Information", info_text)

    # Function to validate data after it is typed
    def on_validate(self, entry, type):
        value = entry.get()
        if type == "stats": 
            if value != "no change" and not (value.isdigit() and int(value) > 0):
                entry.delete(0, tk.END)
                entry.insert(0, "no change")
                messagebox.showwarning("Invalid input", "Please enter a positive integer.")
                return False

        if type == "start_time": 
            if value != "no change":
                if (value.isdigit() and int(value) > 0):
                    if (int(value) > self.duration):
                        entry.delete(0, tk.END)
                        entry.insert(0, "no change")
                        messagebox.showwarning("Invalid input", "Please enter a timestamp in seconds withing the duration of the video.")
                        return False
                else:
                    entry.delete(0, tk.END)
                    entry.insert(0, "no change")
                    messagebox.showwarning("Invalid input", "Please enter a timestamp in seconds withing the duration of the video.")
                    return False

        if type == "label_duration": 
            if value != "no change":
                if (value.isdigit() and int(value) > 0):
                    if self.start_time.get() != "no change":
                        if (self.duration - int(self.start_time.get()) < int(value)):
                            entry.delete(0, tk.END)
                            entry.insert(0, "no change")
                            messagebox.showwarning("Invalid input", "Please enter the the duration of your trimmed video which is less than video's total length minus start time.")
                            return False
                    else:
                        if (int(value) > self.duration):
                            entry.delete(0, tk.END)
                            entry.insert(0, "no change")
                            messagebox.showwarning("Invalid input", "Please enter a value which is less than the duration of the video.")
                            return False

                else:
                    entry.delete(0, tk.END)
                    entry.insert(0, "no change")
                    messagebox.showwarning("Invalid input", "Please enter the the duration in seconds.")
                    return False
        return True

    def start_spinner(self):
        self.running = True
        self.update_spinner()

    def update_spinner(self):
        if not self.running:
            return
        
        current_symbol = self.spinner_label["text"]
        if current_symbol == '😴':
            current_symbol = "/"
        new_symbol = self.spinner_symbols[(self.spinner_symbols.index(current_symbol) + 1) % len(self.spinner_symbols)]
        self.spinner_label.config(text=new_symbol)
        # Update every 100ms
        self.root.after(100, self.update_spinner)  

    def execute_main(self):
        # Create main window
        self.root = tk.Tk()
        self.root.title("Video Processor")

        # Row 0: Video Path Entry
        label_path = tk.Label(self.root, text="Video Path:")
        label_path.grid(row=0, column=0, padx=10, pady=10)
        self.entry_path = tk.Entry(self.root, width=40)
        self.entry_path.grid(row=0, column=1, padx=10, pady=10)
        button_browse = tk.Button(self.root, text="Browse", command=self.select_file)
        button_browse.grid(row=0, column=2, padx=10, pady=10)

        # Row 1: FPS Entry
        label_fps = tk.Label(self.root, text="FPS:")
        label_fps.grid(row=1, column=0, padx=10, pady=5)
        self.entry_fps = tk.Entry(self.root, width=10)
        self.entry_fps.insert(0, "no change")
        self.entry_fps.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        # Row 2: Width Entry
        label_width = tk.Label(self.root, text="Width:")
        label_width.grid(row=2, column=0, padx=10, pady=5)
        self.entry_width = tk.Entry(self.root, width=10)
        self.entry_width.insert(0, "no change")
        self.entry_width.grid(row=2, column=1, sticky="w", padx=10, pady=5)

        # Row 3: Height Entry
        label_height = tk.Label(self.root, text="Height:")
        label_height.grid(row=3, column=0, padx=10, pady=5)
        self.entry_height = tk.Entry(self.root, width=10)
        self.entry_height.insert(0, "no change")
        self.entry_height.grid(row=3, column=1, sticky="w", padx=10, pady=5)

        # Row 4: Start time 
        label_start_time = tk.Label(self.root, text="Start Time:")
        label_start_time.grid(row=4, column=0, padx=10, pady=5)
        self.start_time = tk.Entry(self.root, width=10)
        self.start_time.insert(0, "no change")
        self.start_time.grid(row=4, column=1, sticky="w", padx=10, pady=5)

        # Row 5: End time
        label_duration = tk.Label(self.root, text="Video Duration:")
        label_duration.grid(row=5, column=0, padx=10, pady=5)
        self.label_duration = tk.Entry(self.root, width=10)
        self.label_duration.insert(0, "no change")
        self.label_duration.grid(row=5, column=1, sticky="w", padx=10, pady=5)

        # Row 6: Speed Dropdown
        label_speed = tk.Label(self.root, text="Speed:")
        label_speed.grid(row=6, column=0, padx=10, pady=5)
        self.speed_var = tk.StringVar(self.root)
        speed_options = ["0.25", "0.5", "0.75", "1.25", "1.5", "1.75", "2"]
        self.speed_var.set("no change")  # Set default option
        dropdown_speed = ttk.Combobox(self.root, textvariable=self.speed_var, values=speed_options, state="readonly")
        dropdown_speed.grid(row=6, column=1, sticky="w", padx=10, pady=5)

         # Bind focus-out event to validate entries
        self.entry_fps.bind("<FocusOut>", lambda event: self.on_validate(self.entry_fps, "stats"))
        self.entry_width.bind("<FocusOut>", lambda event: self.on_validate(self.entry_width, "stats"))
        self.entry_height.bind("<FocusOut>", lambda event: self.on_validate(self.entry_height, "stats"))
        self.start_time.bind("<FocusOut>", lambda event: self.on_validate(self.start_time, "start_time"))
        self.label_duration.bind("<FocusOut>", lambda event: self.on_validate(self.label_duration, "label_duration"))

        # Row 7: Buttons - Compress, Process, and Get Info
        button_new = tk.Button(self.root, text="Compress Video", command=lambda: self.start_task("compress"))  
        button_new.grid(row=7, column=1, pady=20, sticky="w") 

        button_process = tk.Button(self.root, text="Process Video", command=lambda: self.start_task("process"))
        button_process.grid(row=7, column=1, pady=20) 

        button_info = tk.Button(self.root, text="Get Info", command=self.get_info)
        button_info.grid(row=7, column=0, pady=20, sticky="")  

        self.spinner_label = tk.Label(self.root, text="😴")
        self.spinner_label.grid(row=7, column=2, pady=10)

        # Run the application
        self.root.mainloop()
