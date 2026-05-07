# Multi-Object Detection and Tracking Pipeline

This repository contains a computer vision pipeline capable of detecting and tracking multiple subjects (people/athletes) in a video using state-of-the-art models. Each detected subject is assigned a unique and persistent ID across frames.

## Approach
- **Object Detection**: YOLOv8s (Ultralytics)
- **Multi-Object Tracking (MOT)**: ByteTrack

ByteTrack is integrated directly into the Ultralytics pipeline, allowing for robust ID assignment even during occlusion or rapid movement.

## Installation

1. **Clone or Extract this repository.**
2. **Set up a Python virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Download a sample video:**
   Run the utility script to download a short cricket video:
   ```bash
   python download_video.py
   ```
   This will download `input_video.mp4`. If you prefer to use your own video, just place it in the project root and name it `input_video.mp4`.

2. **Run the tracker:**
   ```bash
   python tracker.py --input input_video.mp4 --output output_tracked.mp4
   ```
   
   The script will process the video frame-by-frame and generate `output_tracked.mp4` with bounding boxes and unique IDs.

## Limitations & Assumptions
- **Classes**: By default, the tracker is set to only track class `0` (persons). If you need to track vehicles, you must modify the `classes` list in `tracker.py`.
- **Model Size**: YOLOv8s is used for a good balance of speed and accuracy. For higher accuracy (at the cost of speed), you can change it to `yolov8m.pt` or `yolov8l.pt`.
- **Lighting and Quality**: Extremely poor lighting, severe motion blur, or tiny subject scales may lead to dropped tracks or ID switching.

## Deliverables
- `tracker.py`: Main tracking script.
- `download_video.py`: Script to fetch a public domain test video.
- `requirements.txt`: Python dependencies.
- `technical_report.md`: A concise technical overview of the implementation.
- `demo_script.md`: A script to use when recording your video demo.
- `output_tracked.mp4`: Final annotated video (generated after running the tracker).
