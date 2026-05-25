# MP42GIF
Convert MP4 to GIF only


# Portable MP4 to GIF Converter

A lightweight, portable Windows application to convert MP4 videos into high-quality GIFs. 

This tool provides a simple Graphical User Interface (GUI) wrapper around **FFmpeg**. It automatically applies advanced FFmpeg filters (`palettegen` and `paletteuse`) to ensure the resulting GIFs have excellent color quality without massive file sizes.

## ✨ Features
* **Simple GUI:** No command-line knowledge required.
* **Customizable Parameters:** Easily adjust FPS (Frames per second) and Width (Scale) right in the app.
* **High Quality:** Uses 2-pass palette generation to prevent ugly, grainy GIFs.
* **Completely Portable:** No Python installation required for end-users.

## 🚀 How to Use (For End-Users)

If you just want to use the app without touching any code, follow these steps:

1. Go to the **[Releases](../../releases)** page of this repository and download `.exe`.
2. Download `ffmpeg.exe` for Windows from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) (Download the `essentials.zip`, open the `bin` folder, and extract `ffmpeg.exe`).
3. Place **both** files in the exact same folder on your computer. It should look like this:
   ```text
   📁 Your_Folder/
    ┣ 📄 mp4_to_gif.exe
    ┗ 📄 ffmpeg.exe
