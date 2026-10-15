Spooksies Downloader/Converter
Local desktop app for downloading media with gallery-dl and converting M4V files to MP4 with FFmpeg.

Features
Download

Download images and videos using gallery-dl
Choose any output folder
Optional cookies support for sites that require login
Live output log

Convert

Convert single M4V files or entire folders (with subfolders)
Fast remux or full re-encode
Option to overwrite existing MP4s
Option to delete original M4V after successful conversion
Progress bar and log
Test FFmpeg button

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
