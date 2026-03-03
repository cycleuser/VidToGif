"""Command-line interface for vidtogif."""

import argparse
import sys

from vidtogif import __version__
from vidtogif.converter import convert_video_to_gif


def create_parser():
    parser = argparse.ArgumentParser(
        prog="vidtogif",
        description="Convert video files to GIF at original resolution.",
    )
    parser.add_argument(
        "input",
        nargs="?",
        help="Path to the input video file.",
    )
    parser.add_argument(
        "-o", "--output",
        help="Path for the output GIF file. Defaults to <input_name>.gif.",
    )
    parser.add_argument(
        "--fps",
        type=float,
        default=None,
        help="Frames per second for the output GIF (default: video FPS, capped at 30).",
    )
    parser.add_argument(
        "--start",
        type=float,
        default=None,
        help="Start time in seconds.",
    )
    parser.add_argument(
        "--end",
        type=float,
        default=None,
        help="End time in seconds.",
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Launch the graphical user interface.",
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def print_progress(current, total):
    if total <= 0:
        return
    pct = current / total * 100
    bar_len = 40
    filled = int(bar_len * current / total)
    bar = "#" * filled + "-" * (bar_len - filled)
    sys.stdout.write(f"\rProgress: [{bar}] {pct:.1f}%")
    sys.stdout.flush()
    if current >= total:
        sys.stdout.write("\n")


def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.gui:
        from vidtogif.gui import launch_gui
        launch_gui()
        return

    if args.input is None:
        parser.print_help()
        sys.exit(1)

    try:
        print(f"Converting: {args.input}")
        output = convert_video_to_gif(
            input_path=args.input,
            output_path=args.output,
            fps=args.fps,
            start_time=args.start,
            end_time=args.end,
            progress_callback=print_progress,
        )
        print(f"GIF saved to: {output}")
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
