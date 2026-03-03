# VidToGif

A simple and efficient tool to convert any video to GIF at original resolution. Supports both command-line (CLI) and graphical (GUI) interfaces.

[Chinese / 中文文档](README_CN.md)

## Features

- Convert any video format (MP4, AVI, MOV, MKV, WMV, FLV, WebM, etc.) to GIF
- Preserve original video resolution (same-size output)
- Adjustable output FPS
- Optional start/end time trimming
- CLI with progress bar
- GUI with file browser, options panel, and progress indicator
- Cross-platform (Windows, macOS, Linux)

## Installation

### From PyPI

```bash
pip install vidtogif
```

### From source

```bash
git clone https://github.com/cycleuser/Vid2Gif.git
cd Vid2Gif
pip install -r requirements.txt
pip install .
```

## Usage

### CLI

Basic conversion (output defaults to `<input_name>.gif`):

```bash
vidtogif input.mp4
```

Specify output path:

```bash
vidtogif input.mp4 -o output.gif
```

Set output FPS and time range:

```bash
vidtogif input.mp4 --fps 15 --start 2.5 --end 10
```

Run as a Python module:

```bash
python -m vidtogif input.mp4
```

Show help:

```bash
vidtogif --help
```

### GUI

Launch the graphical interface:

```bash
vidtogif --gui
```

Or:

```bash
python -m vidtogif --gui
```

![GUI](images/screen.png)

The GUI provides:

1. **Input Video** - Browse and select any video file
2. **Output GIF** - Choose where to save the GIF (auto-filled)
3. **Options** - Set FPS, start time, and end time
4. **Progress bar** - Real-time conversion progress
5. **Convert button** - Start the conversion

## CLI Reference

```
usage: vidtogif [-h] [-o OUTPUT] [--fps FPS] [--start START] [--end END] [--gui] [-v] [input]

Convert video files to GIF at original resolution.

positional arguments:
  input                 Path to the input video file.

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Path for the output GIF file. Defaults to <input_name>.gif.
  --fps FPS             Frames per second for the output GIF (default: video FPS, capped at 30).
  --start START         Start time in seconds.
  --end END             End time in seconds.
  --gui                 Launch the graphical user interface.
  -v, --version         show program's version number and exit
```

## Requirements

- Python >= 3.8
- opencv-python >= 4.5.0
- Pillow >= 9.0.0
- Tkinter (included with most Python installations, required for GUI only)

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
