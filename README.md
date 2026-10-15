Spooksies Downloader/ConverterA local desktop application for downloading media with gallery-dl and converting M4V files to MP4 using FFmpeg.No file size or count limits. All processing happens on your computer.FeaturesDownload
Download images and videos from supported sites using gallery-dl
Custom output folder
Optional cookies file for authenticated sites
Live output log
Convert
Convert individual M4V files or entire folders (including subfolders)
Fast remux (stream copy) or re-encode for compatibility
Optional overwrite of existing MP4s
Optional deletion of original M4V after successful conversion
Progress bar and conversion log
Test FFmpeg button to verify the executable path
Requirements
Python 3 (Tkinter is included with standard Windows installs)
FFmpeg
gallery-dl (for downloads)
Installation & Usage
Download 
Double-click the file to launch the application
The .pyw version runs without a console window.ConfigurationSettings and cookies are stored in:textDocuments/Spooksies/
├── config.json
└── cookies.txtThis folder is created automatically on first launch.CookiesFor sites that require authentication:
Export cookies from your browser as a Netscape-format cookies.txt file
Place the file at Documents/Spooksies/cookies.txt, or select it inside the app
FFmpeg SetupIf FFmpeg is not detected automatically:
Open the Convert tab
Click Browse next to the FFmpeg path field
Select your ffmpeg.exe
Click Test FFmpeg to confirm it works
The path is saved for future use.Notes
Leaving the output folder empty places converted MP4s in the same directory as the source files
Fast remux is recommended for most M4V to MP4 conversions
Original M4V files are only deleted when the option is explicitly enabled
