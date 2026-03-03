"""Core video-to-GIF conversion logic."""

import os
import cv2
from PIL import Image


def convert_video_to_gif(
    input_path,
    output_path=None,
    fps=None,
    start_time=None,
    end_time=None,
    progress_callback=None,
):
    """Convert a video file to GIF at the original resolution.

    Args:
        input_path: Path to the input video file.
        output_path: Path for the output GIF. Defaults to same name with .gif extension.
        fps: Frames per second for the GIF. Defaults to the video's original FPS (capped at 30).
        start_time: Start time in seconds. Defaults to beginning of video.
        end_time: End time in seconds. Defaults to end of video.
        progress_callback: Optional callable(current_frame, total_frames) for progress updates.

    Returns:
        The path to the generated GIF file.

    Raises:
        FileNotFoundError: If the input file does not exist.
        ValueError: If the input file cannot be opened as a video.
    """
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    if output_path is None:
        base, _ = os.path.splitext(input_path)
        output_path = base + ".gif"

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise ValueError(f"Cannot open video file: {input_path}")

    video_fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if video_fps <= 0:
        video_fps = 25.0

    if fps is None:
        fps = min(video_fps, 30.0)

    # Calculate frame interval to match desired output FPS
    frame_interval = max(1, round(video_fps / fps))
    gif_frame_duration = frame_interval / video_fps  # seconds per GIF frame

    # Calculate start/end frame indices
    start_frame = 0
    end_frame = total_frames
    if start_time is not None:
        start_frame = int(start_time * video_fps)
    if end_time is not None:
        end_frame = int(end_time * video_fps)

    start_frame = max(0, min(start_frame, total_frames))
    end_frame = max(start_frame, min(end_frame, total_frames))

    if start_frame > 0:
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    frames = []
    frame_idx = start_frame
    collected = 0

    while frame_idx < end_frame:
        ret, frame = cap.read()
        if not ret:
            break

        if (frame_idx - start_frame) % frame_interval == 0:
            # Convert BGR (OpenCV) to RGB (PIL)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_frame)
            frames.append(pil_image)
            collected += 1

        frame_idx += 1

        if progress_callback is not None:
            progress_callback(frame_idx - start_frame, end_frame - start_frame)

    cap.release()

    if not frames:
        raise ValueError("No frames were extracted from the video.")

    duration_ms = int(gif_frame_duration * 1000)
    if duration_ms < 20:
        duration_ms = 20  # GIF minimum frame delay

    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration_ms,
        loop=0,
    )

    return output_path
