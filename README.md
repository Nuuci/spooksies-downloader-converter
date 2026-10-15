Spooksies Downloader/Converter
Local desktop app for downloading images & videos with gallery-dl and converting M4V → MP4 with FFmpeg.
![Python](https://img.shields.io/badge/Python-3-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)
No file size or count limits. Everything runs locally on your computer.
---
✨ Features
Download (gallery-dl)
Paste a link and choose a save folder
Optional cookies file for sites that need login
Live output log
Uses the command: `gallery-dl -d "YOUR FOLDER" "LINK"`
Convert (M4V → MP4)
Select individual files or entire folders (with subfolders)
Fast remux (copy streams) or re-encode for maximum compatibility
Optional: overwrite existing MP4s
Optional: delete original M4V after successful conversion
Progress bar + conversion log
Test FFmpeg button to verify your path
---
📋 Requirements
Python 3 (Tkinter is included with most Windows installs)
FFmpeg (or point the app at your `ffmpeg.exe`)
gallery-dl installed and on your PATH (for downloads)
---
🚀 How to Run
Download `spooksies_downloader_converter.pyw`
Double-click it
The `.pyw` file runs without a console window.
> Prefer seeing the console? Use `spooksies_downloader_converter.py` instead.
---
⚙️ Config & Cookies
All settings are stored in:
```
Documents/Spooksies/
├── config.json      ← app settings (auto-created)
└── cookies.txt      ← put your cookies here
```
The folder is created automatically on first launch.
Adding Cookies
For sites that require login (Instagram, Twitter/X, Patreon, etc.):
Export cookies from your browser as a Netscape `cookies.txt` file  
(browser extension: Get cookies.txt LOCALLY or similar)
Save it as `Documents/Spooksies/cookies.txt`  
or browse to it inside the app
---
🔧 FFmpeg Path
If the app doesn’t find FFmpeg automatically:
Go to the Convert tab
Click Browse… next to FFmpeg path
Select your `ffmpeg.exe`
Click Test FFmpeg to confirm it works
The path is saved and remembered for next time.
---
💡 Tips
Leave the Output folder empty on the Convert tab to place MP4s next to the original files.
Use Fast remux for speed (usually perfect for M4V → MP4).
Use Re-encode only when you need maximum player compatibility.
Original M4V files are only deleted if you check the box.
---
📁 Project Files
File	Description
`spooksies_downloader_converter.pyw`	Main app — double-click to run (no console)
`spooksies_downloader_converter.py`	Same app (shows console if preferred)
`README.md`	This file
---
📜 License
MIT — free to use and modify.
