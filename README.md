# 秒速画像変換 — Byousoku Image Converter

A premium, lightweight Windows desktop application for lightning-fast image processing. Convert, resize, compress, and batch process images with a modern bilingual (Japanese/English) interface.

![Platform](https://img.shields.io/badge/platform-Windows%2010%2F11-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![License](https://img.shields.io/badge/license-MIT-yellow)

---

## Download

**[⬇ Download Latest Release](https://drive.google.com/file/d/18eehb2MmoFWfcDXMnMMo8yDNsR6OlZUw/view?usp=sharing)**

| Version | Format | Size |
|---|---|---|
| v2.0.0 | Windows Installer (.exe) | ~25 MB |

---

## Features

### 画像変換 — Format Convert
Convert between PNG, JPG, and WebP with EXIF metadata preservation. Transparent PNG → JPG automatically composites onto white background.

### 画像縮小 — Image Resize
Three modes: percentage (10-200%), pixel dimensions, or presets (SNS, Blog, Email, Wallpaper, Icon). Uses LANCZOS resampling for professional quality.

### 画像圧縮 — Image Compress
Quality slider (1-100) with live before/after size estimation. Supports lossless PNG optimization and lossy compression for all formats.

### HEIC変換 — HEIC to JPG/PNG
Convert Apple HEIC/HEIF photos to standard formats. Auto-rotation based on EXIF orientation.

### 一括処理 — Batch Process
Process entire folders at once with multi-threaded execution (up to 8 workers). Includes file rename pattern engine and recursive subfolder scanning.

---

## Screenshots

<!-- Add screenshots here -->

---

## Installation

### Installer (Recommended)
1. Download the installer from [Releases](https://drive.google.com/file/d/18eehb2MmoFWfcDXMnMMo8yDNsR6OlZUw/view?usp=sharing)
2. Run the .exe installer
3. Follow the setup wizard

### Run from Source
```bash
git clone https://github.com/YOUR_USERNAME/byousoku-image.git
cd byousoku-image
pip install -r requirements.txt
python main.py
```

### Build Your Own
```bash
build.bat          # Portable EXE
build_installer.bat # EXE + Windows installer
```

---

## Requirements

- Windows 10/11 (64-bit)
- No internet connection required — fully offline

**For development:**
- Python 3.9+
- customtkinter, Pillow, pillow-heif, tkinterdnd2

---

## License

[MIT License](LICENSE.txt)

---

## Built With

- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) — Modern UI framework
- [Pillow](https://python-pillow.org/) — Image processing
- [pillow-heif](https://github.com/uploadcare/pillow-heif) — HEIC support
- [tkinterdnd2](https://github.com/pmgagne/tkinterdnd2) — Drag & drop
- [PyInstaller](https://pyinstaller.org/) — Executable packaging
- [Inno Setup](https://jrsoftware.org/isinfo.php) — Windows installer
