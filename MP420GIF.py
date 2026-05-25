import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import sys

def get_base_path():
    """Gets the folder where the .exe or script is running."""
    if getattr(sys, 'frozen', False):
        # If running as a compiled .exe
        return os.path.dirname(sys.executable)
    else:
        # If running as a .py script
        return os.path.dirname(os.path.abspath(__file__))

def select_file():
    global input_path
    input_path = filedialog.askopenfilename(
        title="Select MP4 Video",
        filetypes=[("MP4 Files", "*.mp4"), ("All Files", "*.*")]
    )
    if input_path:
        file_label.config(text=f"Selected: {os.path.basename(input_path)}")
        status_label.config(text="Ready to convert.", fg="blue")

def convert_to_gif():
    if not input_path:
        messagebox.showwarning("No File", "Please select an MP4 file first.")
        return

    # Validate parameters
    try:
        fps_val = int(fps_var.get())
        scale_val = int(scale_var.get())
        if fps_val <= 0 or scale_val <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Input", "FPS and Width must be valid positive numbers.")
        return

    output_path = filedialog.asksaveasfilename(
        title="Save GIF As",
        defaultextension=".gif",
        filetypes=[("GIF Files", "*.gif")]
    )
    
    if not output_path:
        return

    status_label.config(text="Converting... Please wait.", fg="orange")
    root.update()

    # Look for ffmpeg.exe in the same directory as this app
    base_path = get_base_path()
    ffmpeg_path = os.path.join(base_path, 'ffmpeg.exe')

    if not os.path.exists(ffmpeg_path):
        messagebox.showerror("Error", f"ffmpeg.exe not found!\n\nPlease make sure ffmpeg.exe is in the exact same folder as this application:\n{base_path}")
        status_label.config(text="Error: ffmpeg.exe missing.", fg="red")
        return

    # Create the FFmpeg filter string using user inputs
    filter_complex = f"fps={fps_val},scale={scale_val}:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse"

    command = [
        ffmpeg_path,
        '-y', 
        '-i', input_path,
        '-vf', filter_complex,
        '-loop', '0',
        output_path
    ]

    try:
        # Prevent the black CMD window from popping up on Windows
        creationflags = 0
        if os.name == 'nt':
            creationflags = subprocess.CREATE_NO_WINDOW

        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=creationflags)
        status_label.config(text="Conversion Complete!", fg="green")
        messagebox.showinfo("Success", f"GIF successfully saved to:\n{output_path}")
        
    except subprocess.CalledProcessError as e:
        status_label.config(text="Conversion Failed.", fg="red")
        messagebox.showerror("Error", "An error occurred during conversion.\nMake sure the video file is not corrupted.")

# --- GUI Layout ---
root = tk.Tk()
root.title("Portable MP4 to GIF")
root.geometry("450x330")
root.resizable(False, False)

input_path = ""

tk.Label(root, text="MP4 to GIF Converter", font=("Arial", 16, "bold")).pack(pady=10)

# 1. Select Button
tk.Button(root, text="1. Select MP4 File", command=select_file, font=("Arial", 11), width=20).pack(pady=5)
file_label = tk.Label(root, text="No file selected", fg="gray")
file_label.pack()

# --- Parameters Frame ---
param_frame = tk.Frame(root)
param_frame.pack(pady=15)

tk.Label(param_frame, text="FPS (Frames/sec):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
fps_var = tk.StringVar(value="15")
tk.Entry(param_frame, textvariable=fps_var, width=10).grid(row=0, column=1, padx=5, pady=5)

tk.Label(param_frame, text="Width (Pixels):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
scale_var = tk.StringVar(value="480")
tk.Entry(param_frame, textvariable=scale_var, width=10).grid(row=1, column=1, padx=5, pady=5)
# ------------------------

# 2. Convert Button
tk.Button(root, text="2. Convert & Save GIF", command=convert_to_gif, font=("Arial", 11), width=20, bg="#4CAF50", fg="black").pack(pady=5)

status_label = tk.Label(root, text="", font=("Arial", 10, "italic"))
status_label.pack(pady=5)

root.mainloop()