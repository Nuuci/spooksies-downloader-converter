# spooksies-downloader-converter
A downloader and converter tool made using Python
Spooksies Downloader/Converter
Local desktop app for downloading images/videos with gallery-dl and converting M4V → MP4 with FFmpeg.
No file size or count limits. Everything runs on your computer.
---
Requirements
Python 3 (with Tkinter — included in most Windows installs)
FFmpeg installed (or you can point the app at `ffmpeg.exe`)
gallery-dl installed and on your PATH (for downloads)
---
How to Run
Download `spooksies_downloader_converter.pyw`
Double-click it
The `.pyw` file runs without a black console window.
---
Features
Download tab (gallery-dl)
Paste a link and choose a save folder
Optional cookies file for sites that need login
Uses: `gallery-dl -d "YOUR FOLDER" "LINK"`
Live output log
Convert tab (M4V → MP4)
Select individual files or an entire folder (with subfolders)
Fast remux (copy streams) or re-encode for max compatibility
Optional: overwrite existing MP4s
Optional: delete original M4V after successful conversion
Progress bar + log
Test FFmpeg button to verify your path
---
Config & Cookies
All settings are stored in:
```
Documents\Spooksies\
├── config.json      ← app settings
└── cookies.txt      ← put your cookies here
```
The folder is created automatically the first time you run the app.
Cookies
For sites that require login (Instagram, Twitter/X, Patreon, etc.):
Export cookies from your browser as a Netscape `cookies.txt` file  
(use an extension like “Get cookies.txt LOCALLY”)
Put the file in `Documents\Spooksies\cookies.txt`  
or browse to it in the app
---
FFmpeg Path
If the app doesn’t find FFmpeg automatically:
Go to the Convert tab
Click Browse… next to FFmpeg path
Select your `ffmpeg.exe`
Click Test FFmpeg to confirm it works
The path is saved and remembered.
---
Tips
Leave Output folder empty on the Convert tab to put MP4s next to the original files.
Use Fast remux for speed (usually fine for M4V → MP4).
Use Re-encode only if you need maximum compatibility.
The app will not delete original M4Vs unless you check the box.
---
Files
File	Purpose
`spooksies_downloader_converter.pyw`	Run this (no console)
`spooksies_downloader_converter.py`	Same app, shows console if you prefer
