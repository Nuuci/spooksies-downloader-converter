#!/usr/bin/env python3
"""
Spooksies Downloader/Converter
Local desktop app for:
- Downloading images/videos with gallery-dl
- Converting video files to other formats with FFmpeg
Config is stored in Documents/Spooksies/
"""
import os
import sys
import json
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
import shutil

# Hide console windows for child processes on Windows
CREATE_NO_WINDOW = 0x08000000 if sys.platform == "win32" else 0

# Config location: Documents/Spooksies/
DOCUMENTS = Path.home() / "Documents"
CONFIG_DIR = DOCUMENTS / "Spooksies"
CONFIG_FILE = CONFIG_DIR / "config.json"
COOKIES_FILE = CONFIG_DIR / "cookies.txt"

# Common video extensions FFmpeg can handle
VIDEO_EXTS = {
    ".mp4", ".m4v", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm",
    ".ts", ".m2ts", ".mts", ".mpg", ".mpeg", ".mpe", ".3gp", ".ogv",
    ".divx", ".vob", ".asf", ".rm", ".rmvb", ".f4v"
}

# Recommended conversion settings per output format
FORMAT_SETTINGS = {
    "mp4": {
        "ext": ".mp4",
        "copy": ["-c", "copy", "-movflags", "+faststart"],
        "encode": [
            "-c:v", "libx264", "-crf", "23", "-preset", "medium",
            "-c:a", "aac", "-b:a", "128k", "-pix_fmt", "yuv420p",
            "-movflags", "+faststart"
        ],
        "note": "Best overall compatibility (H.264 + AAC)"
    },
    "mkv": {
        "ext": ".mkv",
        "copy": ["-c", "copy"],
        "encode": [
            "-c:v", "libx264", "-crf", "23", "-preset", "medium",
            "-c:a", "aac", "-b:a", "128k"
        ],
        "note": "Flexible container, good for most codecs"
    },
    "mov": {
        "ext": ".mov",
        "copy": ["-c", "copy", "-movflags", "+faststart"],
        "encode": [
            "-c:v", "libx264", "-crf", "23", "-preset", "medium",
            "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart"
        ],
        "note": "Apple-friendly (similar to MP4)"
    },
    "webm": {
        "ext": ".webm",
        "copy": ["-c", "copy"],
        "encode": [
            "-c:v", "libvpx-vp9", "-crf", "30", "-b:v", "0",
            "-c:a", "libopus", "-b:a", "128k"
        ],
        "note": "Web-optimized (VP9 + Opus)"
    },
    "avi": {
        "ext": ".avi",
        "copy": ["-c", "copy"],
        "encode": [
            "-c:v", "mpeg4", "-qscale:v", "3",
            "-c:a", "mp3", "-b:a", "128k"
        ],
        "note": "Older compatibility (MPEG-4 + MP3)"
    },
}

class SpooksiesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Spooksies Downloader/Converter")
        self.root.geometry("850x700")
        self.root.minsize(750, 600)

        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        self.load_config()

        self.ffmpeg_path = self.find_tool("ffmpeg")
        self.gallery_dl_path = self.find_tool("gallery-dl")

        if not self.ffmpeg_path:
            messagebox.showwarning(
                "FFmpeg Not Found",
                "FFmpeg was not found automatically.\n\n"
                "On the Convert tab, use the 'FFmpeg path' box and click Browse…\n"
                "to select your ffmpeg.exe file.\n\n"
                "Common locations:\n"
                "C:\\ffmpeg\\bin\\ffmpeg.exe\n"
                "Downloads folder, Desktop, etc."
            )
        if not self.gallery_dl_path:
            messagebox.showwarning(
                "gallery-dl",
                "gallery-dl not found. Downloads will not work.\nInstall it and add to PATH."
            )

        self.files_to_convert = []
        self.is_converting = False
        self.is_downloading = False

        self.build_ui()
        self.load_settings_into_ui()

    def find_tool(self, name):
        """Find executable using multiple methods."""
        found = shutil.which(name)
        if found:
            return found
        found = shutil.which(f"{name}.exe")
        if found:
            return found

        if sys.platform == "win32":
            try:
                result = subprocess.run(
                    ["where", name],
                    capture_output=True, text=True, timeout=10,
                    creationflags=CREATE_NO_WINDOW
                )
                if result.returncode == 0:
                    path = result.stdout.strip().splitlines()[0].strip()
                    if path and Path(path).is_file():
                        return path
            except Exception:
                pass

        home = Path.home()
        candidates = [
            rf"C:\{name}\bin\{name}.exe",
            rf"C:\Program Files\{name}\bin\{name}.exe",
            rf"C:\Program Files (x86)\{name}\bin\{name}.exe",
            rf"C:\tools\{name}\bin\{name}.exe",
            home / name / "bin" / f"{name}.exe",
            home / "Downloads" / name / "bin" / f"{name}.exe",
            home / "Downloads" / f"{name}.exe",
            home / "Desktop" / name / "bin" / f"{name}.exe",
            home / "Desktop" / f"{name}.exe",
            home / "Documents" / name / "bin" / f"{name}.exe",
            Path(os.environ.get("LOCALAPPDATA", "")) / name / "bin" / f"{name}.exe",
            Path(os.environ.get("APPDATA", "")) / name / "bin" / f"{name}.exe",
            Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "WinGet" / "Links" / f"{name}.exe",
            Path("C:/ProgramData/chocolatey/bin") / f"{name}.exe",
            home / "scoop" / "apps" / name / "current" / f"{name}.exe",
            home / "scoop" / "shims" / f"{name}.exe",
        ]

        search_roots = [
            Path("C:/"),
            Path("C:/Program Files"),
            Path("C:/Program Files (x86)"),
            home / "Downloads",
            home / "Desktop",
            home / "Documents",
            Path(os.environ.get("LOCALAPPDATA", "")),
            Path(os.environ.get("APPDATA", "")),
        ]
        for root in search_roots:
            if not root.exists():
                continue
            try:
                for item in root.iterdir():
                    if item.is_dir() and name.lower() in item.name.lower():
                        for sub in [item / "bin" / f"{name}.exe", item / f"{name}.exe"]:
                            if sub.is_file():
                                candidates.append(sub)
            except (PermissionError, OSError):
                continue

        for p in candidates:
            p = Path(p)
            if p.is_file():
                return str(p)
        return None

    def load_config(self):
        self.config = {
            "download_folder": str(Path.home() / "Downloads" / "Spooksies"),
            "cookies_path": str(COOKIES_FILE),
            "conversion_mode": "copy",
            "output_format": "mp4",
            "delete_after": False,
            "overwrite": False,
            "recursive": True,
        }
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    self.config.update(loaded)
            except Exception:
                pass
        if not COOKIES_FILE.exists():
            COOKIES_FILE.write_text(
                "# Netscape HTTP Cookie File\n# Paste your cookies here (from browser export)\n",
                encoding="utf-8"
            )

    def save_config(self):
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            messagebox.showerror("Config", f"Could not save config:\n{e}")

    def build_ui(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # ===== DOWNLOAD TAB =====
        download_frame = ttk.Frame(notebook, padding=15)
        notebook.add(download_frame, text="Download (gallery-dl)")

        ttk.Label(download_frame, text="Download videos & pictures with gallery-dl",
                  font=("Segoe UI", 12, "bold")).pack(anchor=tk.W, pady=(0, 10))

        url_frame = ttk.Frame(download_frame)
        url_frame.pack(fill=tk.X, pady=5)
        ttk.Label(url_frame, text="Link / URL:").pack(side=tk.LEFT)
        self.url_var = tk.StringVar()
        ttk.Entry(url_frame, textvariable=self.url_var, width=70).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        folder_frame = ttk.Frame(download_frame)
        folder_frame.pack(fill=tk.X, pady=5)
        ttk.Label(folder_frame, text="Save to folder:").pack(side=tk.LEFT)
        self.download_folder_var = tk.StringVar()
        ttk.Entry(folder_frame, textvariable=self.download_folder_var, width=55).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(folder_frame, text="Browse…", command=self.browse_download_folder).pack(side=tk.LEFT)

        cookies_frame = ttk.Frame(download_frame)
        cookies_frame.pack(fill=tk.X, pady=5)
        ttk.Label(cookies_frame, text="Cookies file:").pack(side=tk.LEFT)
        self.cookies_var = tk.StringVar()
        ttk.Entry(cookies_frame, textvariable=self.cookies_var, width=55).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(cookies_frame, text="Browse…", command=self.browse_cookies).pack(side=tk.LEFT)
        ttk.Button(cookies_frame, text="Open Config Folder", command=self.open_config_folder).pack(side=tk.LEFT, padx=5)

        ttk.Label(download_frame, text="Tip: Put your cookies.txt in Documents\\Spooksies\\cookies.txt",
                  foreground="gray").pack(anchor=tk.W, pady=(0, 10))

        self.download_btn = ttk.Button(download_frame, text="Download", command=self.start_download)
        self.download_btn.pack(pady=10)

        log_frame = ttk.LabelFrame(download_frame, text="Output", padding=5)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        self.download_log = scrolledtext.ScrolledText(log_frame, height=12, font=("Consolas", 9))
        self.download_log.pack(fill=tk.BOTH, expand=True)

        # ===== CONVERT TAB =====
        convert_frame = ttk.Frame(notebook, padding=15)
        notebook.add(convert_frame, text="Convert Videos")

        ttk.Label(convert_frame, text="Convert videos to other formats",
                  font=("Segoe UI", 12, "bold")).pack(anchor=tk.W, pady=(0, 10))

        btn_frame = ttk.Frame(convert_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame, text="Select Files…", command=self.select_files).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Select Folder…", command=self.select_folder).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear List", command=self.clear_list).pack(side=tk.LEFT, padx=5)

        list_frame = ttk.LabelFrame(convert_frame, text="Files to Convert", padding=5)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        self.file_listbox = tk.Listbox(list_frame, selectmode=tk.EXTENDED, font=("Consolas", 9))
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        self.file_listbox.configure(yscrollcommand=scrollbar.set)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        options = ttk.LabelFrame(convert_frame, text="Options", padding=10)
        options.pack(fill=tk.X, pady=5)

        # Output format
        format_frame = ttk.Frame(options)
        format_frame.pack(fill=tk.X, pady=2)
        ttk.Label(format_frame, text="Output format:").pack(side=tk.LEFT)
        self.format_var = tk.StringVar(value="mp4")
        self.format_combo = ttk.Combobox(
            format_frame,
            textvariable=self.format_var,
            values=list(FORMAT_SETTINGS.keys()),
            state="readonly",
            width=10
        )
        self.format_combo.pack(side=tk.LEFT, padx=5)
        self.format_combo.bind("<<ComboboxSelected>>", self.on_format_changed)
        self.format_note = ttk.Label(format_frame, text="", foreground="gray")
        self.format_note.pack(side=tk.LEFT, padx=10)

        # Mode
        mode_frame = ttk.Frame(options)
        mode_frame.pack(fill=tk.X, pady=2)
        ttk.Label(mode_frame, text="Mode:").pack(side=tk.LEFT)
        self.mode_var = tk.StringVar(value="copy")
        ttk.Radiobutton(mode_frame, text="Fast remux (copy streams)", variable=self.mode_var, value="copy").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(mode_frame, text="Re-encode (recommended)", variable=self.mode_var, value="encode").pack(side=tk.LEFT, padx=10)

        opt_frame = ttk.Frame(options)
        opt_frame.pack(fill=tk.X, pady=2)
        self.recursive_var = tk.BooleanVar(value=True)
        self.overwrite_var = tk.BooleanVar(value=False)
        self.delete_after_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(opt_frame, text="Include subfolders", variable=self.recursive_var).pack(side=tk.LEFT, padx=(0, 15))
        ttk.Checkbutton(opt_frame, text="Overwrite existing files", variable=self.overwrite_var).pack(side=tk.LEFT, padx=(0, 15))
        ttk.Checkbutton(opt_frame, text="Delete original after success", variable=self.delete_after_var).pack(side=tk.LEFT)

        # FFmpeg path
        ffmpeg_frame = ttk.Frame(options)
        ffmpeg_frame.pack(fill=tk.X, pady=5)
        ttk.Label(ffmpeg_frame, text="FFmpeg path:").pack(side=tk.LEFT)
        self.ffmpeg_path_var = tk.StringVar()
        ttk.Entry(ffmpeg_frame, textvariable=self.ffmpeg_path_var, width=50).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(ffmpeg_frame, text="Browse…", command=self.browse_ffmpeg).pack(side=tk.LEFT)
        ttk.Label(ffmpeg_frame, text="(leave empty to auto-detect)", foreground="gray").pack(side=tk.LEFT, padx=5)

        # Output folder
        out_frame = ttk.Frame(options)
        out_frame.pack(fill=tk.X, pady=5)
        ttk.Label(out_frame, text="Output folder:").pack(side=tk.LEFT)
        self.convert_output_var = tk.StringVar()
        ttk.Entry(out_frame, textvariable=self.convert_output_var, width=50).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(out_frame, text="Browse…", command=self.browse_convert_output).pack(side=tk.LEFT)
        ttk.Label(out_frame, text="(empty = same folder)", foreground="gray").pack(side=tk.LEFT, padx=5)

        self.progress = ttk.Progressbar(convert_frame, mode="determinate")
        self.progress.pack(fill=tk.X, pady=5)
        self.status_label = ttk.Label(convert_frame, text="Ready.", foreground="gray")
        self.status_label.pack(anchor=tk.W)

        self.convert_log = scrolledtext.ScrolledText(convert_frame, height=6, font=("Consolas", 8))
        self.convert_log.pack(fill=tk.BOTH, expand=False, pady=5)

        btn_row = ttk.Frame(convert_frame)
        btn_row.pack(pady=5)
        self.convert_btn = ttk.Button(btn_row, text="Convert", command=self.start_conversion)
        self.convert_btn.pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_row, text="Test FFmpeg", command=self.test_ffmpeg).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_row, text="Save Settings", command=self.save_settings_from_ui).pack(side=tk.LEFT, padx=5)

        self.status_bar = ttk.Label(self.root, text=f"Config: {CONFIG_DIR}", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def on_format_changed(self, event=None):
        fmt = self.format_var.get()
        if fmt in FORMAT_SETTINGS:
            self.format_note.config(text=FORMAT_SETTINGS[fmt]["note"])
            # Prefer re-encode as the safer recommended default when switching formats
            if self.mode_var.get() == "copy":
                self.mode_var.set("encode")
        self.save_settings_from_ui()

    def load_settings_into_ui(self):
        self.download_folder_var.set(self.config.get("download_folder", ""))
        self.cookies_var.set(self.config.get("cookies_path", str(COOKIES_FILE)))
        self.mode_var.set(self.config.get("conversion_mode", "copy"))
        self.format_var.set(self.config.get("output_format", "mp4"))
        self.delete_after_var.set(self.config.get("delete_after", False))
        self.overwrite_var.set(self.config.get("overwrite", False))
        self.recursive_var.set(self.config.get("recursive", True))

        saved_ffmpeg = self.config.get("ffmpeg_path", "")
        if saved_ffmpeg and Path(saved_ffmpeg).is_file():
            self.ffmpeg_path = saved_ffmpeg
            self.ffmpeg_path_var.set(saved_ffmpeg)
        elif self.ffmpeg_path:
            self.ffmpeg_path_var.set(self.ffmpeg_path)

        self.on_format_changed()

    def save_settings_from_ui(self):
        self.config["download_folder"] = self.download_folder_var.get().strip()
        self.config["cookies_path"] = self.cookies_var.get().strip()
        self.config["conversion_mode"] = self.mode_var.get()
        self.config["output_format"] = self.format_var.get()
        self.config["delete_after"] = self.delete_after_var.get()
        self.config["overwrite"] = self.overwrite_var.get()
        self.config["recursive"] = self.recursive_var.get()

        manual = self.ffmpeg_path_var.get().strip()
        if manual:
            self.config["ffmpeg_path"] = manual
            self.ffmpeg_path = manual
        self.save_config()

    # ----- Download methods -----
    def browse_download_folder(self):
        folder = filedialog.askdirectory(title="Select download folder")
        if folder:
            self.download_folder_var.set(folder)

    def browse_cookies(self):
        path = filedialog.askopenfilename(title="Select cookies.txt", filetypes=[("Text", "*.txt"), ("All", "*.*")])
        if path:
            self.cookies_var.set(path)

    def open_config_folder(self):
        if sys.platform == "win32":
            os.startfile(CONFIG_DIR)
        else:
            subprocess.run(["open" if sys.platform == "darwin" else "xdg-open", str(CONFIG_DIR)])

    def start_download(self):
        url = self.url_var.get().strip()
        folder = self.download_folder_var.get().strip()
        if not url:
            messagebox.showwarning("Missing URL", "Please enter a link to download.")
            return
        if not folder:
            messagebox.showwarning("Missing folder", "Please choose a save folder.")
            return
        if not self.gallery_dl_path:
            messagebox.showerror("gallery-dl", "gallery-dl not found. Please install it.")
            return
        if self.is_downloading:
            return
        Path(folder).mkdir(parents=True, exist_ok=True)
        self.save_settings_from_ui()
        self.is_downloading = True
        self.download_btn.config(state=tk.DISABLED)
        self.download_log.delete(1.0, tk.END)
        self.download_log.insert(tk.END, f"Downloading to: {folder}\nURL: {url}\n\n")
        thread = threading.Thread(target=self.run_download, args=(url, folder), daemon=True)
        thread.start()

    def run_download(self, url, folder):
        cmd = [self.gallery_dl_path, "-d", folder, url]
        cookies = self.cookies_var.get().strip()
        if cookies and Path(cookies).is_file():
            cmd.extend(["--cookies", cookies])
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                creationflags=CREATE_NO_WINDOW
            )
            for line in process.stdout:
                self.root.after(0, lambda l=line: self.download_log.insert(tk.END, l) or self.download_log.see(tk.END))
            process.wait()
            self.root.after(0, lambda: self.download_log.insert(tk.END, f"\nFinished with code {process.returncode}\n"))
        except Exception as e:
            self.root.after(0, lambda: self.download_log.insert(tk.END, f"\nError: {e}\n"))
        finally:
            self.is_downloading = False
            self.root.after(0, lambda: self.download_btn.config(state=tk.NORMAL))

    # ----- Convert methods -----
    def select_files(self):
        video_types = " ".join(f"*{ext}" for ext in sorted(VIDEO_EXTS))
        files = filedialog.askopenfilenames(
            title="Select video files",
            filetypes=[("Video files", video_types), ("All files", "*.*")]
        )
        if files:
            self.add_files(files)

    def select_folder(self):
        folder = filedialog.askdirectory(title="Select folder")
        if folder:
            self.add_folder(folder)

    def browse_convert_output(self):
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self.convert_output_var.set(folder)

    def browse_ffmpeg(self):
        path = filedialog.askopenfilename(
            title="Select ffmpeg.exe",
            filetypes=[("FFmpeg", "ffmpeg.exe"), ("Executable", "*.exe"), ("All files", "*.*")]
        )
        if path:
            self.ffmpeg_path_var.set(path)
            self.ffmpeg_path = path
            self.save_settings_from_ui()

    def test_ffmpeg(self):
        path = self.ffmpeg_path_var.get().strip().strip('"')
        if not path:
            path = self.ffmpeg_path or ""
        if not path or not Path(path).is_file():
            messagebox.showerror("Test", "No valid FFmpeg path set.")
            return
        try:
            result = subprocess.run(
                [path, "-version"],
                capture_output=True, text=True, timeout=10,
                creationflags=CREATE_NO_WINDOW
            )
            if result.returncode == 0:
                ver = result.stdout.splitlines()[0] if result.stdout else "OK"
                messagebox.showinfo("Test FFmpeg", f"Works!\n\n{ver}")
                self.convert_log.insert(tk.END, f"Test OK: {ver}\n")
            else:
                messagebox.showerror("Test FFmpeg", f"Failed:\n{result.stderr[:400]}")
        except Exception as e:
            messagebox.showerror("Test FFmpeg", f"Could not run:\n{e}")

    def add_files(self, paths):
        added = 0
        for path in paths:
            p = Path(path)
            if p.suffix.lower() in VIDEO_EXTS and str(p) not in self.files_to_convert:
                self.files_to_convert.append(str(p))
                self.file_listbox.insert(tk.END, str(p))
                added += 1
        self.status_label.config(text=f"Added {added}. Total: {len(self.files_to_convert)}")

    def add_folder(self, folder):
        folder = Path(folder)
        recursive = self.recursive_var.get()
        added = 0
        pattern = "**/*" if recursive else "*"
        for f in folder.glob(pattern):
            if f.is_file() and f.suffix.lower() in VIDEO_EXTS and str(f) not in self.files_to_convert:
                self.files_to_convert.append(str(f))
                self.file_listbox.insert(tk.END, str(f))
                added += 1
        self.status_label.config(text=f"Added {added} from folder. Total: {len(self.files_to_convert)}")

    def clear_list(self):
        self.files_to_convert.clear()
        self.file_listbox.delete(0, tk.END)
        self.status_label.config(text="List cleared.")

    def start_conversion(self):
        manual = self.ffmpeg_path_var.get().strip().strip('"')
        if manual and Path(manual).is_file():
            self.ffmpeg_path = manual
        if not self.ffmpeg_path or not Path(self.ffmpeg_path).is_file():
            messagebox.showerror("FFmpeg", "Valid FFmpeg path not set.\nUse Browse or Test FFmpeg first.")
            return
        if not self.files_to_convert:
            messagebox.showwarning("No files", "Select files or a folder first.")
            return
        if self.is_converting:
            return

        fmt = self.format_var.get()
        if fmt not in FORMAT_SETTINGS:
            messagebox.showerror("Format", "Please select a valid output format.")
            return

        self.save_settings_from_ui()
        self.is_converting = True
        self.convert_btn.config(state=tk.DISABLED)
        self.progress["value"] = 0
        self.progress["maximum"] = len(self.files_to_convert)
        self.convert_log.delete(1.0, tk.END)
        self.convert_log.insert(tk.END, f"Using FFmpeg: {self.ffmpeg_path}\n")
        self.convert_log.insert(tk.END, f"Output format: {fmt.upper()} ({FORMAT_SETTINGS[fmt]['note']})\n")
        self.convert_log.insert(tk.END, f"Mode: {self.mode_var.get()}\n\n")
        thread = threading.Thread(target=self.convert_all, daemon=True)
        thread.start()

    def convert_all(self):
        success = failed = 0
        total = len(self.files_to_convert)
        mode = self.mode_var.get()
        fmt = self.format_var.get()
        settings = FORMAT_SETTINGS[fmt]
        overwrite = self.overwrite_var.get()
        delete_after = self.delete_after_var.get()
        out_dir_str = self.convert_output_var.get().strip()
        last_error = ""

        extra_args = settings["encode"] if mode == "encode" else settings["copy"]

        for i, input_str in enumerate(self.files_to_convert):
            input_path = Path(input_str)
            self.update_status(f"Converting {i+1}/{total}: {input_path.name}")

            if out_dir_str:
                out_dir = Path(out_dir_str)
                out_dir.mkdir(parents=True, exist_ok=True)
                output_path = out_dir / (input_path.stem + settings["ext"])
            else:
                output_path = input_path.with_suffix(settings["ext"])

            if output_path.exists() and not overwrite:
                self.update_status(f"Skipped (exists): {output_path.name}")
                success += 1
                self.update_progress(i + 1)
                continue

            cmd = [
                self.ffmpeg_path,
                "-y" if overwrite else "-n",
                "-i", str(input_path),
                *extra_args,
                str(output_path)
            ]

            try:
                self.convert_log_insert(f"Running: {' '.join(cmd)}\n")
                result = subprocess.run(
                    cmd,
                    capture_output=True, text=True, timeout=None,
                    creationflags=CREATE_NO_WINDOW
                )
                if result.returncode == 0 and output_path.exists():
                    success += 1
                    self.convert_log_insert(f"OK: {output_path.name}\n")
                    if delete_after:
                        try:
                            input_path.unlink()
                        except Exception:
                            pass
                else:
                    failed += 1
                    err = (result.stderr or result.stdout or "Unknown error")[-600:]
                    last_error = f"{input_path.name}: {err}"
                    self.convert_log_insert(f"FAIL: {err}\n")
                    self.update_status(f"Failed: {input_path.name}")
            except Exception as e:
                failed += 1
                last_error = str(e)
                self.convert_log_insert(f"ERROR: {e}\n")
                self.update_status(f"Error: {input_path.name}")

            self.update_progress(i + 1)

        self.is_converting = False
        self.root.after(0, self.on_conversion_done, success, failed, total, last_error)

    def convert_log_insert(self, text):
        self.root.after(0, lambda: self.convert_log.insert(tk.END, text) or self.convert_log.see(tk.END))

    def update_status(self, text):
        self.root.after(0, lambda: self.status_label.config(text=text))

    def update_progress(self, value):
        self.root.after(0, lambda: self.progress.configure(value=value))

    def on_conversion_done(self, success, failed, total, last_error=""):
        self.convert_btn.config(state=tk.NORMAL)
        msg = f"Finished!\n\nSuccessful: {success}\nFailed: {failed}\nTotal: {total}"
        if last_error and failed > 0:
            msg += f"\n\nLast error:\n{last_error[:500]}"
        self.status_label.config(text=f"Done — {success} succeeded, {failed} failed.")
        if failed == 0:
            messagebox.showinfo("Complete", msg)
        else:
            messagebox.showwarning("Complete with errors", msg)

def main():
    root = tk.Tk()
    style = ttk.Style()
    if "vista" in style.theme_names():
        style.theme_use("vista")
    elif "clam" in style.theme_names():
        style.theme_use("clam")
    app = SpooksiesApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
