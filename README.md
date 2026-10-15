# Spooksies Downloader/Converter

Local desktop app for downloading images & videos with **gallery-dl** and converting **M4V → MP4** with **FFmpeg**.

![Python](https://img.shields.io/badge/Python-3-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)

No file size or count limits. Everything runs locally on your computer.

---

## ✨ Features

### Download (gallery-dl)
- Paste a link and choose a save folder
- Optional cookies file for sites that need login
- Live output log
- Uses the command: `gallery-dl -d "YOUR FOLDER" "LINK"`

  <img width="893" height="781" alt="image" src="https://github.com/user-attachments/assets/66fa6a71-9fc5-40c1-86f2-20044742775b" />



### Convert (M4V → MP4)
- Select individual files or entire folders (with subfolders)
- Fast remux (copy streams) or re-encode for maximum compatibility
- Optional: overwrite existing MP4s
- Optional: delete original M4V after successful conversion
- Progress bar + conversion log
- **Test FFmpeg** button to verify your path

  <img width="893" height="778" alt="image" src="https://github.com/user-attachments/assets/b763c1d7-b2bb-4cc0-860a-c2a5e8f9b745" />


---

## 📋 Requirements

- **Python 3** (Tkinter is included with most Windows installs)
- **FFmpeg** (or point the app at your `ffmpeg.exe`)
- **gallery-dl** installed and on your PATH (for downloads)

---

## How to Download & Run

1. Click the green **Code** button at the top right of this repo
2. Click **Download ZIP**
3. Unzip the downloaded file
4. Open the unzipped folder and find `spooksies_downloader_converter.pyw`
5. Double-click it to run the app

The `.pyw` file runs without a console window.

---

## ⚙️ Config & Cookies

All settings are stored in:

```
Documents/Spooksies/
├── config.json      ← app settings (auto-created)
└── cookies.txt      ← put your cookies here
```

The folder is created automatically on first launch.

### Adding Cookies

For sites that require login (Instagram, Twitter/X, Patreon, etc.):

1. Export cookies from your browser as a Netscape `cookies.txt` file  
   (browser extension: *Get cookies.txt LOCALLY* or similar)
2. Save it as `Documents/Spooksies/cookies.txt`  
   **or** browse to it inside the app

---

## 🔧 FFmpeg Path

If the app doesn’t find FFmpeg automatically:

1. Go to the **Convert** tab
2. Click **Browse…** next to **FFmpeg path**
3. Select your `ffmpeg.exe`
4. Click **Test FFmpeg** to confirm it works

The path is saved and remembered for next time.

---

## 💡 Tips

- Leave the **Output folder** empty on the Convert tab to place MP4s next to the original files.
- Use **Fast remux** for speed (usually perfect for M4V → MP4).
- Use **Re-encode** only when you need maximum player compatibility.
- Original M4V files are only deleted if you check the box.

---

## 📁 Project Files

| File | Description |
|------|-------------|
| `spooksies_downloader_converter.pyw` | Main app — double-click to run (no console) |
| `spooksies_downloader_converter.py` | Same app (shows console if preferred) |
| `README.md` | This file |

---

## 📜 License

MIT — free to use and modify.
