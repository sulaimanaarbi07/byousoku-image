# 秒速画像変換 — Byousoku Image Converter

## Complete User Documentation & Technical Reference

**Version:** 2.0.0
**Platform:** Windows 10/11
**Language:** Python 3.14 + CustomTkinter
**License:** MIT

---

## Table of Contents

1. [Overview](#overview)
2. [System Requirements](#system-requirements)
3. [Installation](#installation)
4. [Getting Started](#getting-started)
5. [Interface Overview](#interface-overview)
6. [Feature 1: Image Convert (画像変換)](#feature-1-image-convert)
7. [Feature 2: Image Resize (画像縮小)](#feature-2-image-resize)
8. [Feature 3: Image Compress (画像圧縮)](#feature-3-image-compress)
9. [Feature 4: HEIC Convert (HEIC変換)](#feature-4-heic-convert)
10. [Feature 5: Batch Process (一括処理)](#feature-5-batch-process)
11. [Settings Panel](#settings-panel)
12. [File Drag & Drop](#file-drag--drop)
13. [Building from Source](#building-from-source)
14. [Creating the Installer](#creating-the-installer)
15. [Troubleshooting](#troubleshooting)
16. [Technical Architecture](#technical-architecture)

---

## Overview

秒速画像変換 (Byousoku Image Converter) is a premium, lightweight Windows desktop application for fast image processing. It provides five core operations: format conversion, resizing, compression, HEIC conversion, and batch folder processing.

**Key Highlights:**
- Modern dark/light UI with Japanese and English localization
- Drag & drop file support
- Multi-threaded batch processing for speed
- Live compression size estimation
- Preserve or strip EXIF metadata
- No internet connection required — fully offline

---

## System Requirements

| Requirement | Minimum |
|---|---|
| OS | Windows 10 or later (64-bit) |
| RAM | 4 GB |
| Disk Space | 200 MB (for installed app) |
| Display | 1280x720 or higher |

**For running from source:**
- Python 3.9 or later
- pip (Python package manager)

---

## Installation

### Option A: Installer (Recommended)

1. Download `秒速画像変換_Setup_v2.0.0.exe`
2. Double-click to run the installer
3. Follow the setup wizard:
   - Choose installation directory (default: `C:\Program Files\ByousokuImageConverter`)
   - Optionally create a desktop shortcut
   - Optionally associate image files (.png, .jpg, .webp) with the app
4. Click Install
5. Launch from Start Menu or desktop shortcut

### Option B: Portable (No Install)

1. Copy the entire `dist/秒速画像変換/` folder to any location
2. Run `秒速画像変換.exe` inside the folder
3. Settings are saved as `settings.json` next to the executable

### Option C: Run from Source

1. Ensure Python 3.9+ is installed and in your PATH
2. Open a terminal in the project directory
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run:
   ```
   python main.py
   ```

---

## Getting Started

### First Launch

When you first open the app:

1. The window appears centered on your screen (860x640 pixels)
2. The interface loads in Japanese by default
3. The **画像変換 (Convert)** tab is shown by default
4. Dark theme is applied automatically

### Quick Workflow

The simplest workflow:

1. **Add files** — drag images onto the drop zone, or click "ファイルを追加"
2. **Configure options** — set output format, quality, size, etc. on the right panel
3. **Click "処理を開始"** — the blue button at bottom-right
4. **Wait for completion** — a progress bar shows real-time status
5. **Open output folder** — click "保存先フォルダを開く" to see results

---

## Interface Overview

The application window is divided into four sections:

```
+------------------------------------------------------+
|  秒速画像変換                              [⚙ Settings] |  ← Top Bar
+------------------------------------------------------+
|  [画像変換] [画像縮小] [画像圧縮] [HEIC変換] [一括処理] |  ← Tab Selector
+------------------------------------------------------+
|                                                      |
|   LEFT PANEL          |    RIGHT PANEL               |
|   (File List Area)    |    (Options & Settings)      |
|                       |                              |
|   [Drop Zone]         |    Format: [PNG ▼]           |
|   ┌─────────────────┐ |    [✓] Preserve metadata     |
|   │ photo1.png 2.1MB│ |    [Add Files]               |
|   │ photo2.jpg 1.4MB│ |    [Clear List]              |
|   └─────────────────┘ |                              |
|                                                      |
+------------------------------------------------------+
|  Ready                           [Open Folder] [Start]|  ← Bottom Bar
|  ████████████████░░░░░░░░░░░░░░░░░                    |
+------------------------------------------------------+
```

### Top Bar
- **App Title** — "秒速画像変換" (or English equivalent)
- **Settings Gear (⚙)** — Opens the full settings panel

### Tab Selector
A segmented button with 5 tabs:
- **画像変換** — Format conversion
- **画像縮小** — Image resizing
- **画像圧縮** — Image compression
- **HEIC変換** — HEIC/HEIF to JPG/PNG
- **一括処理** — Batch folder processing

### Bottom Bar
- **Status text** — Shows current state (Ready, Processing X/Y, Done)
- **Progress bar** — Visual progress indicator
- **Open Save Folder** — Opens the output directory in Windows Explorer
- **Start Process** — Begins processing (changes to Cancel during operation)

---

## Feature 1: Image Convert

**Tab Name:** 画像変換 (Convert)

**Purpose:** Convert images between PNG, JPG, and WebP formats.

### Supported Input Formats
- PNG (.png)
- JPEG (.jpg, .jpeg)
- WebP (.webp)

### Step-by-Step

1. **Switch to the Convert tab** — Click "画像変換" in the tab bar

2. **Add images** — Use one of three methods:
   - **Drag & Drop:** Drag image files from Windows Explorer onto the drop zone
   - **Add Files button:** Click "ファイルを追加" to open a file picker
   - Both methods support multi-select

3. **Review file list** — Each file shows:
   - File name (truncated if longer than 40 characters)
   - File size in KB or MB
   - Delete button (✕) to remove individual files

4. **Configure output format** — On the right panel:
   - **出力フォーマット (Output Format):** Select from dropdown:
     - `PNG` — Lossless, supports transparency
     - `JPG` — Lossy, smaller files, no transparency
     - `WEBP` — Modern format, excellent compression

5. **Metadata option:**
   - **[✓] メタデータ(EXIF等)を保持する** — When checked, preserves EXIF data (camera info, GPS, date taken)
   - Uncheck to strip all metadata for privacy

6. **Click "処理を開始" (Start Process)**

7. **Results:**
   - Files are saved to the configured output folder
   - Original filenames are preserved with new extensions
   - A success dialog appears when complete

### Technical Details

- **Transparency handling:** When converting PNG (with transparency) to JPG, the alpha channel is composited onto a white background. This prevents black artifacts.
- **JPEG quality:** Fixed at 90 (high quality)
- **WebP quality:** Fixed at 85
- **PNG:** Uses optimization flag for smaller file sizes

---

## Feature 2: Image Resize

**Tab Name:** 画像縮小 (Resize)

**Purpose:** Scale images to different dimensions using three modes.

### Step-by-Step

1. **Switch to the Resize tab** — Click "画像縮小"

2. **Add images** — Same drag & drop or file picker methods

3. **Choose resize mode** — Select from the "サイズ指定方法" dropdown:

   **Mode A: Percentage (比率指定)**
   - A slider appears (10% to 200%)
   - Drag the slider to scale images proportionally
   - Example: 50% on a 1920x1080 image = 960x540
   - Aspect ratio is always maintained

   **Mode B: Dimensions (ピクセル指定)**
   - Two input fields appear: Width and Height
   - Enter exact pixel values (default: 1920x1080)
   - **アスペクト比を維持する (Preserve Aspect Ratio):** When checked, the image fits within the specified dimensions while maintaining proportions (using the smaller ratio)

   **Mode C: Presets (プリセット指定)**
   - Choose from predefined sizes:
     - `SNS (1200x630)` — Social media sharing
     - `Blog (800x600)` — Blog post images
     - `Email (640x480)` — Email attachments
     - `Wallpaper (1920x1080)` — Desktop wallpaper
     - `Icon (256x256)` — Application icons

4. **Metadata option:**
   - **[✓] メタデータ(EXIF等)を保持する** — Preserve or strip EXIF

5. **Click "処理を開始"**

### Technical Details

- Uses **LANCZOS resampling** for the highest quality downscaling
- Minimum output size is 1x1 pixel (prevents zero-size errors)
- Original file format is preserved (PNG stays PNG, JPG stays JPG)
- The aspect ratio checkbox only appears in Dimensions mode (hidden for Percentage and Presets, where it's implicitly handled)

---

## Feature 3: Image Compress

**Tab Name:** 画像圧縮 (Compress)

**Purpose:** Reduce image file sizes with adjustable quality settings and live size estimation.

### Step-by-Step

1. **Switch to the Compress tab** — Click "画像圧縮"

2. **Add images** — Same methods as other tabs

3. **Set compression quality:**
   - **圧縮品質 (1-100):** A slider from 1 (maximum compression, lowest quality) to 100 (minimum compression, highest quality)
   - Default value: 80
   - The current value is displayed next to the slider in accent color

4. **Lossless option:**
   - **[✓] 可逆圧縮 (PNG等でサイズ削減のみ)** — For PNG files only
   - When checked: uses PNG optimization without losing any quality
   - When unchecked: applies lossy compression (reduces color palette for PNG, adjusts quality for JPG/WebP)

5. **Review size estimation:**
   - The **推定サイズ (Estimated Size)** card shows:
     - **圧縮前 (Before Size):** Total size of all added files
     - **圧縮後 (After Size):** Estimated total size after compression, with percentage reduction
   - Estimation updates live as you adjust the quality slider
   - Runs in a background thread to prevent UI freezing

6. **Click "処理を開始"**

### Compression Behavior by Format

| Format | Lossy Mode | Lossless Mode |
|---|---|---|
| **JPEG** | Quality slider (1-100) + optimize flag | N/A (always lossy) |
| **WebP** | Quality slider (1-100) | True lossless WebP |
| **PNG** | Color quantization (if quality < 80) | optimize=True, compress_level=9 |

### Technical Details

- Size estimation saves to an in-memory buffer (no disk I/O) for speed
- EXIF metadata is always preserved during compression
- Color quantization for PNG uses: `min(256, max(16, int(2.5 * quality)))` colors

---

## Feature 4: HEIC Convert

**Tab Name:** HEIC変換 (HEIC to JPG/PNG)

**Purpose:** Convert Apple HEIC/HEIF photos to standard JPG or PNG format.

### What is HEIC?
HEIC (High Efficiency Image Container) is the default photo format on iPhones and iPads since iOS 11. While efficient, it's not universally supported. This tool converts HEIC to widely-compatible formats.

### Step-by-Step

1. **Switch to the HEIC tab** — Click "HEIC変換"

2. **Add HEIC files:**
   - Drag & drop only accepts `.heic` and `.heif` files
   - File picker filters to show only HEIC/HEIF files
   - **Note:** Other image formats are automatically rejected in this tab

3. **Choose target format:**
   - **JPG (JPEG):** Smaller files, no transparency, universal compatibility
   - **PNG:** Larger files, supports transparency, lossless

4. **Auto-rotate option:**
   - **[✓] EXIF情報に基づいて自動回転する** — When checked, images are automatically rotated based on the EXIF orientation tag
   - This fixes photos that appear sideways after conversion

5. **Click "処理を開始"**

### Dependency Warning
If `pillow-heif` is not installed, a red warning appears:
```
⚠️ pillow-heif is not installed!
HEIC conversion will fail.
```
Install it with: `pip install pillow-heif`

### Technical Details

- Uses `pillow-heif` library with `register_heif_opener()` for seamless Pillow integration
- Auto-rotation uses `PIL.ImageOps.exif_transpose()` (EXIF tag 274)
- When converting to JPG, RGBA transparency is composited onto white background
- JPEG output quality: 90
- PNG output: optimized with `optimize=True`

---

## Feature 5: Batch Process

**Tab Name:** 一括処理 (Batch Process)

**Purpose:** Process entire folders of images at once, with any of the four operations.

### Step-by-Step

1. **Switch to the Batch tab** — Click "一括処理"

2. **Select source folder:**
   - Click "フォルダ選択" to browse for a folder
   - Or type/paste a path directly into the text field
   - The folder is automatically scanned when selected

3. **Configure scanning:**
   - **[✓] サブフォルダも再帰的に検索する** — Scan all subfolders recursively
   - **[✓] オリジナルファイルを残す** — Keep original files (don't overwrite)

4. **Review scan results:**
   - The status card shows:
     - Folder name
     - Number of matching files found
     - Breakdown by file extension (e.g., "PNG: 45枚, JPG: 120枚")
   - Scanning updates automatically when you change the operation type (HEIC vs standard images)

5. **Choose batch operation** — Select from "一括処理アクション" dropdown:

   **Convert (画像変換):**
   - Output format: PNG, JPG, or WEBP

   **Resize (画像縮小):**
   - Mode: Percentage (10-200% slider) or Presets (SNS, Blog, Email, Wallpaper)

   **Compress (画像圧縮):**
   - Quality slider (1-100)

   **HEIC to JPG/PNG (HEIC変換):**
   - Target format: JPG or PNG

6. **Set rename pattern (optional):**
   - **ファイル名パターン:** Enter a pattern like `prefix_{name}_suffix`
   - `{name}` is replaced with the original filename (without extension)
   - Invalid characters (\/:*?"<>|) are automatically removed
   - If a file with the new name already exists, a counter is appended: `_1`, `_2`, etc.

7. **Metadata option:**
   - **[✓] メタデータ(EXIF等)を保持する**

8. **Click "処理を開始"**

### Technical Details

- Uses Python's `ThreadPoolExecutor` for parallel processing
- Worker count: `min(cpu_count, 8)` threads
- Progress updates in real-time (current file / total files)
- Cancellation is supported mid-batch (remaining files are skipped)
- Files are processed as they complete (not in order), using `as_completed()`

---

## Settings Panel

**Access:** Click the ⚙ gear icon in the top-right corner

### Available Settings

| Setting | Description | Options |
|---|---|---|
| **言語 (Language)** | Interface language | 日本語 (Japanese), English |
| **テーマ (Theme)** | Visual theme | ダーク (Dark), ライト (Light), システム連動 (System) |
| **デフォルト圧縮品質** | Default compression quality | Slider: 1-100 |
| **デフォルト保存先** | Default output folder | Any folder path, with Browse button |

### How Settings Work

1. **Language:** Changes take effect immediately in the settings panel for preview. Click "保存" (Save) to apply globally. All tabs, buttons, and messages update instantly without restarting.

2. **Theme:**
   - **Dark:** Deep blue-black background (#121222) with hot pink accent (#e94560)
   - **Light:** Clean white background (#f5f5f7) with blue accent (#007aff)
   - **System:** Follows Windows system theme

3. **Default Quality:** Sets the initial quality value for the Compress tab's slider.

4. **Default Output Folder:** Where all processed files are saved.
   - Default: `Pictures/ByousokuConverted` in the user's home directory
   - Falls back to `~/ByousokuConverted` if Pictures folder doesn't exist
   - Can be changed to any writable directory

### Settings Storage

Settings are saved to `settings.json` in the application directory:
```json
{
    "language": "ja",
    "theme": "Dark",
    "default_quality": 85,
    "default_output_dir": "C:\\Users\\username\\Pictures\\ByousokuConverted"
}
```

---

## File Drag & Drop

The application supports native drag & drop using `tkinterdnd2`.

### How It Works

1. **Drag files** from Windows Explorer onto the drop zone
2. The drop zone border highlights in accent color when you hover
3. Drop to add all valid files
4. Files with unsupported extensions are silently ignored
5. Duplicate files are not added twice

### Supported File Types per Tab

| Tab | Accepted Extensions |
|---|---|
| Convert | .png, .jpg, .jpeg, .webp |
| Resize | .png, .jpg, .jpeg, .webp |
| Compress | .png, .jpg, .jpeg, .webp |
| HEIC | .heic, .heif |
| Batch | Depends on selected operation |

### Fallback Behavior

If `tkinterdnd2` is not installed or the tkdnd native library is missing:
- The drop zone text changes to show only the "Add Files" instruction
- All other functionality works normally via file picker dialogs
- No error is shown — graceful degradation

---

## Building from Source

### Prerequisites

```
pip install pyinstaller pillow-heif customtkinter tkinterdnd2 pillow
```

### Build Steps

1. **Quick build:** Double-click `build.bat`
   - Installs dependencies
   - Runs PyInstaller with icon and proper naming
   - Output: `dist/秒速画像変換/`

2. **Manual build:**
   ```
   pyinstaller --noconfirm --onedir --windowed --clean ^
       --name "秒速画像変換" ^
       --icon "assets/icon.ico" ^
       --add-data "locales;locales" ^
       --add-data "assets;assets" ^
       main.py
   ```

### Build Options

| Option | Meaning |
|---|---|
| `--onedir` | Output as a folder (faster launch, recommended) |
| `--onefile` | Single .exe (slower launch, larger size) |
| `--windowed` | No console window (GUI app) |
| `--icon` | Application icon (.ico file) |
| `--add-data` | Bundle extra files (locales, assets) |

---

## Creating the Installer

### Prerequisites

1. Download and install [Inno Setup 6](https://jrsoftware.org/isinfo.php) (free)
2. Build the application first (run `build.bat`)

### Steps

1. **Option A — Using build.bat:** The build script auto-detects Inno Setup and creates the installer automatically.

2. **Option B — Manual:**
   - Open `installer.iss` in Inno Setup
   - Click **Build > Compile** (or press Ctrl+F9)
   - Output: `installer_output/秒速画像変換_Setup_v2.0.0.exe`

3. **Option C — Command line:**
   ```
   "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
   ```

### Installer Features

- **Multilingual:** Japanese and English installer UI
- **Start Menu shortcuts** created automatically
- **Optional desktop shortcut**
- **Optional file associations** for .png, .jpg, .jpeg, .webp
- **Clean uninstall** removes all files and registry entries
- **LZMA2 compression** for smallest installer size
- **Modern wizard style**

---

## Troubleshooting

### Common Issues

**"No files added for processing"**
- You clicked Start without adding any files
- Solution: Add files via drag & drop or the Add Files button

**HEIC conversion fails**
- `pillow-heif` is not installed
- Solution: `pip install pillow-heif`

**Drag & Drop doesn't work**
- `tkinterdnd2` native library is missing
- Solution: Reinstall tkinterdnd2: `pip install --force-reinstall tkinterdnd2`
- Fallback: Use the "Add Files" button instead

**App doesn't start**
- Missing dependencies
- Solution: `pip install -r requirements.txt`

**Output files not found**
- Check the default output folder in Settings
- Click "Open Save Folder" in the bottom bar to navigate there

**Processing seems slow**
- Large files take longer to process
- Batch mode uses multi-threading but is still I/O bound on HDD
- Use an SSD for best performance

### Error Messages

| Message | Meaning |
|---|---|
| `err_no_files` | No files were added to process |
| `err_invalid_format` | A file has an unsupported extension |
| `err_invalid_dimensions` | Width/height values are not valid numbers |
| `err_process_failed` | Some files could not be processed |

---

## Technical Architecture

### Project Structure

```
byousoku-image/
├── main.py                  # Entry point, window setup, icon loading
├── requirements.txt         # Python dependencies
├── build.bat                # Build script (PyInstaller + optional Inno Setup)
├── installer.iss            # Inno Setup installer script
├── LICENSE.txt              # MIT license
├── settings.json            # User settings (created at runtime)
│
├── assets/
│   ├── icon.png             # App icon (1024x1024 PNG)
│   └── icon.ico             # App icon (multi-size ICO: 16-256px)
│
├── core/
│   ├── converter.py         # Format conversion (PNG/JPG/WebP)
│   ├── resizer.py           # Image resizing (LANCZOS)
│   ├── compressor.py        # Image compression + size estimation
│   ├── heic_converter.py    # HEIC/HEIF to JPG/PNG
│   └── batch_processor.py   # Thread pool orchestrator
│
├── ui/
│   ├── app.py               # Main app frame, tab routing, action handler
│   ├── top_bar.py           # Header with title and settings button
│   ├── bottom_bar.py        # Progress bar, status, action buttons
│   ├── settings_panel.py    # Settings overlay (language, theme, paths)
│   ├── theme.py             # Colors, fonts, radii constants
│   ├── widgets.py           # Reusable widgets (DragDrop, FileList, QualitySlider)
│   ├── tab_convert.py       # Convert tab UI
│   ├── tab_resize.py        # Resize tab UI
│   ├── tab_compress.py      # Compress tab UI
│   ├── tab_heic.py          # HEIC tab UI
│   └── tab_batch.py         # Batch tab UI
│
├── locales/
│   ├── manager.py           # Singleton translation manager
│   ├── ja.py                # Japanese strings
│   └── en.py                # English strings
│
└── dist/
    └── 秒速画像変換/         # PyInstaller output (portable app)
```

### Technology Stack

| Component | Technology |
|---|---|
| Language | Python 3.14 |
| UI Framework | CustomTkinter (modern Tkinter wrapper) |
| Image Processing | Pillow (PIL) + pillow-heif |
| Drag & Drop | tkinterdnd2 (tkdnd wrapper) |
| Concurrency | ThreadPoolExecutor (stdlib) |
| Packaging | PyInstaller 6.20 |
| Installer | Inno Setup 6 |

### Processing Pipeline

```
User Input (files + params)
        ↓
   App.get_payload()
        ↓
   BatchProcessor.start_batch()
        ↓
   ThreadPoolExecutor (N workers)
        ↓
   ┌──────────────────────────────┐
   │ Per-file processing:          │
   │  converter.convert_image()    │
   │  resizer.resize_image()       │
   │  compressor.compress_image()  │
   │  heic_converter.convert()     │
   └──────────────────────────────┘
        ↓
   Optional rename (pattern engine)
        ↓
   progress_callback → UI update
        ↓
   complete_callback → show result dialog
```

### Color Scheme

**Dark Theme:**
| Element | Color |
|---|---|
| Background | #121222 |
| Surface | #1a1a2e |
| Accent | #e94560 (hot pink) |
| Text Primary | #ffffff |
| Text Secondary | #a0a5c0 |
| Border | #2a2a40 |
| Success | #4caf50 |

**Light Theme:**
| Element | Color |
|---|---|
| Background | #f5f5f7 |
| Surface | #ffffff |
| Accent | #007aff (blue) |
| Text Primary | #1c1c1e |
| Text Secondary | #8e8e93 |
| Border | #e5e5e7 |
| Success | #34c759 |

### Font Stack

- **Windows:** Yu Gothic UI (supports Japanese characters)
- **Other platforms:** Segue UI fallback

---

*This documentation covers 秒速画像変換 version 2.0.0. Generated 2026-05-25.*
