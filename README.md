Spooksies Downloader/Converter
Local desktop app for downloading media with gallery-dl and converting M4V files to MP4 with FFmpeg.

Features
Download

Download images and videos using gallery-dl
Choose any output folder
Optional cookies support for sites that require login
Live output log

<img width="796" height="675" alt="image" src="https://github.com/user-attachments/assets/ddbfec24-532c-445e-80b5-41ca8e143cb6" />



Convert

Convert single M4V files or entire folders (with subfolders)
Fast remux or full re-encode
Option to overwrite existing MP4s
Option to delete original M4V after successful conversion
Progress bar and log
Test FFmpeg button

<img width="901" height="746" alt="image" src="https://github.com/user-attachments/assets/dc5f9703-028b-4ab3-bf51-bca5482f5d02" />



Requirements

Python 3
FFmpeg
gallery-dl (for downloads)

How to Run
Download  and double-click it.

Configuration
All settings are stored in:
Documents/Spooksies/

config.json — app settings
cookies.txt — place your cookies file here

Setting the FFmpeg Path
If FFmpeg is not found automatically:

Go to the Convert tab
Click Browse next to the FFmpeg path field
Select your ffmpeg.exe
Click Test FFmpeg

The path is remembered.

Notes

Leave the output folder empty to save MP4s next to the original files.
Fast remux is recommended for most conversions.
Original files are only deleted if you enable the option.
