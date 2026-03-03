"""Graphical user interface for vidtogif using Tkinter."""

import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from vidtogif.converter import convert_video_to_gif

VIDEO_EXTENSIONS = (
    ("Video files", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm *.m4v *.mpeg *.mpg *.3gp"),
    ("All files", "*.*"),
)


class VidToGifApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VidToGif - Video to GIF Converter")
        self.root.resizable(True, True)
        self.root.minsize(520, 360)

        self._build_ui()
        self._center_window(560, 380)

    def _center_window(self, w, h):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _build_ui(self):
        pad = {"padx": 8, "pady": 4}

        # --- Input file ---
        frame_input = ttk.LabelFrame(self.root, text="Input Video")
        frame_input.pack(fill="x", **pad)

        self.var_input = tk.StringVar()
        ttk.Entry(frame_input, textvariable=self.var_input).pack(
            side="left", fill="x", expand=True, padx=(8, 4), pady=6
        )
        ttk.Button(frame_input, text="Browse...", command=self._browse_input).pack(
            side="right", padx=(4, 8), pady=6
        )

        # --- Output file ---
        frame_output = ttk.LabelFrame(self.root, text="Output GIF")
        frame_output.pack(fill="x", **pad)

        self.var_output = tk.StringVar()
        ttk.Entry(frame_output, textvariable=self.var_output).pack(
            side="left", fill="x", expand=True, padx=(8, 4), pady=6
        )
        ttk.Button(frame_output, text="Browse...", command=self._browse_output).pack(
            side="right", padx=(4, 8), pady=6
        )

        # --- Options ---
        frame_opts = ttk.LabelFrame(self.root, text="Options")
        frame_opts.pack(fill="x", **pad)

        row0 = ttk.Frame(frame_opts)
        row0.pack(fill="x", padx=8, pady=4)

        ttk.Label(row0, text="FPS:").pack(side="left")
        self.var_fps = tk.StringVar()
        ttk.Entry(row0, textvariable=self.var_fps, width=8).pack(side="left", padx=(4, 16))
        ttk.Label(row0, text="(Leave empty for auto)").pack(side="left")

        row1 = ttk.Frame(frame_opts)
        row1.pack(fill="x", padx=8, pady=4)

        ttk.Label(row1, text="Start (sec):").pack(side="left")
        self.var_start = tk.StringVar()
        ttk.Entry(row1, textvariable=self.var_start, width=8).pack(side="left", padx=(4, 16))

        ttk.Label(row1, text="End (sec):").pack(side="left")
        self.var_end = tk.StringVar()
        ttk.Entry(row1, textvariable=self.var_end, width=8).pack(side="left", padx=(4, 8))

        # --- Progress ---
        frame_prog = ttk.Frame(self.root)
        frame_prog.pack(fill="x", **pad)

        self.progress = ttk.Progressbar(frame_prog, mode="determinate", maximum=100)
        self.progress.pack(fill="x", padx=8, pady=4)

        self.var_status = tk.StringVar(value="Ready")
        ttk.Label(frame_prog, textvariable=self.var_status).pack(padx=8)

        # --- Convert button ---
        self.btn_convert = ttk.Button(self.root, text="Convert", command=self._start_convert)
        self.btn_convert.pack(pady=10)

    def _browse_input(self):
        path = filedialog.askopenfilename(filetypes=VIDEO_EXTENSIONS)
        if path:
            self.var_input.set(path)
            if not self.var_output.get():
                base, _ = os.path.splitext(path)
                self.var_output.set(base + ".gif")

    def _browse_output(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".gif",
            filetypes=[("GIF files", "*.gif"), ("All files", "*.*")],
        )
        if path:
            self.var_output.set(path)

    def _parse_optional_float(self, value):
        value = value.strip()
        if not value:
            return None
        return float(value)

    def _start_convert(self):
        input_path = self.var_input.get().strip()
        output_path = self.var_output.get().strip() or None

        if not input_path:
            messagebox.showwarning("Warning", "Please select an input video file.")
            return

        try:
            fps = self._parse_optional_float(self.var_fps.get())
            start = self._parse_optional_float(self.var_start.get())
            end = self._parse_optional_float(self.var_end.get())
        except ValueError:
            messagebox.showerror("Error", "FPS, Start, and End must be valid numbers.")
            return

        self.btn_convert.configure(state="disabled")
        self.progress["value"] = 0
        self.var_status.set("Converting...")

        thread = threading.Thread(
            target=self._run_convert,
            args=(input_path, output_path, fps, start, end),
            daemon=True,
        )
        thread.start()

    def _run_convert(self, input_path, output_path, fps, start, end):
        def progress_cb(current, total):
            if total > 0:
                pct = current / total * 100
                self.root.after(0, self._update_progress, pct)

        try:
            result = convert_video_to_gif(
                input_path=input_path,
                output_path=output_path,
                fps=fps,
                start_time=start,
                end_time=end,
                progress_callback=progress_cb,
            )
            self.root.after(0, self._on_success, result)
        except Exception as e:
            self.root.after(0, self._on_error, str(e))

    def _update_progress(self, pct):
        self.progress["value"] = pct
        self.var_status.set(f"Converting... {pct:.1f}%")

    def _on_success(self, output_path):
        self.progress["value"] = 100
        self.var_status.set("Done!")
        self.btn_convert.configure(state="normal")
        messagebox.showinfo("Success", f"GIF saved to:\n{output_path}")

    def _on_error(self, error_msg):
        self.var_status.set("Error")
        self.btn_convert.configure(state="normal")
        messagebox.showerror("Error", error_msg)


def launch_gui():
    root = tk.Tk()
    VidToGifApp(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()
