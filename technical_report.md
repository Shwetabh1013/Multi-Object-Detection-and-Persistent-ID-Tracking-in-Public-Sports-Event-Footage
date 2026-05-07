# Technical Report: Multi-Object Detection and Tracking Pipeline

## Overview
This report outlines the architecture and design decisions behind the multi-object tracking pipeline implemented for public event/sports footage. The pipeline detects relevant subjects (e.g., players, athletes) and assigns them unique, persistent IDs that track their movement across frames.

## 1. Model and Algorithm Selection
### Detection: YOLOv8
We utilized **YOLOv8s** (You Only Look Once, version 8 small) for the object detection phase. YOLOv8 is the latest state-of-the-art model in the YOLO family, developed by Ultralytics. 
- **Why YOLOv8?** It offers an unparalleled trade-off between inference speed and detection accuracy. In dynamic sports and public event footage, subjects can move rapidly and adopt unusual poses. YOLOv8's anchor-free detection mechanism makes it highly resilient to these variations. The "small" variant (YOLOv8s) was chosen because it allows for near real-time processing on standard consumer hardware without a significant drop in precision compared to the larger models.

### Tracking: ByteTrack
For multi-object tracking (MOT), we integrated **ByteTrack**. 
- **Why ByteTrack?** Traditional trackers like SORT or DeepSORT often discard detection boxes with low confidence scores. This is problematic during partial occlusions (e.g., when one player steps in front of another), as the occluded person's confidence score drops, leading to broken trajectories and ID switches. ByteTrack solves this by utilizing *all* detection boxes. It first matches high-scoring boxes to existing tracks. Then, instead of discarding the low-scoring boxes, it associates them with unmatched tracks to recover heavily occluded subjects. 
- **ID Consistency**: ByteTrack maintains ID consistency through Kalman Filtering (to predict the next location of a track) combined with Hungarian Algorithm matching based on Intersection over Union (IoU).

## 2. Pipeline Architecture
1. **Frame Extraction**: The video is read frame-by-frame using OpenCV.
2. **Inference**: Each frame is passed through the YOLOv8 network. We filter the detections strictly for the `person` class (Class ID 0 in the COCO dataset) to avoid false positives from background objects.
3. **Data Association**: The bounding boxes and confidence scores are fed into the ByteTrack algorithm. ByteTrack compares the new detections with the predicted locations of previously established tracks and assigns IDs.
4. **Annotation & Output**: Bounding boxes, confidence scores, and persistent unique IDs are drawn onto the frame using Ultralytics' plotting utilities, and the frame is written to an output video file.

## 3. Challenges Faced & Failure Cases
While testing on public video samples, several common real-world challenges were observed:
- **Severe Occlusion**: When a dense cluster of people forms, overlapping bounding boxes can sometimes cause the tracker to briefly swap IDs (ID Switching). While ByteTrack mitigates this better than previous algorithms, a complete occlusion lasting several seconds will still result in the tracker assigning a new ID when the subject reappears.
- **Scale Changes and Camera Motion**: Rapid camera zooming or panning can abruptly shift the relative position of all subjects, challenging the Kalman Filter's linear motion assumptions.
- **Motion Blur**: In fast-paced sports clips, subjects sprinting across the screen can blur, dropping their detection confidence entirely for a few frames.

## 4. Possible Improvements
To further enhance the robustness of this pipeline in a production environment, the following enhancements could be implemented:
1. **Appearance Matching (Re-ID)**: Integrating a Re-Identification (Re-ID) model (like OSNet or BoT-SORT) would allow the tracker to remember the visual features of a subject. If a track is lost due to long-term occlusion, a Re-ID model can re-assign the correct ID when the subject reappears based on their appearance (e.g., jersey color).
2. **Camera Motion Compensation (CMC)**: Utilizing algorithms like ECC (Enhanced Correlation Coefficient) to estimate background movement would correct the camera motion before updating the Kalman Filter, significantly improving tracking during camera pans.
3. **Trajectory Smoothing**: Applying a Savitzky-Golay filter to the tracking outputs as a post-processing step to smooth out jitter in bounding box coordinates.
