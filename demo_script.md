# Demo Video Script Outline

*Note: You must record yourself speaking over a screen capture for the 3-5 minute demo. Use this script as a guide.*

---

**[0:00 - 0:30] Introduction**
- *Visual*: Show the code repository / IDE.
- *Voiceover*: "Hi, this is a demonstration of my multi-object tracking pipeline designed for public event and sports footage. The goal of this project was to detect all people in a video and assign them unique, persistent IDs, handling challenges like occlusion and motion blur."

**[0:30 - 1:30] Approach & Architecture**
- *Visual*: Open `tracker.py` and highlight the YOLO initialization and ByteTrack parameters.
- *Voiceover*: "For the architecture, I chose YOLOv8 for object detection because of its state-of-the-art speed and accuracy. For the tracking algorithm, I integrated ByteTrack. The reason I chose ByteTrack over algorithms like DeepSORT is that ByteTrack doesn't throw away low-confidence bounding boxes. Instead, it uses them to maintain tracks during partial occlusions, which is very common in sports when players cross paths. I restricted the detection classes strictly to the 'person' class to avoid false positives."

**[1:30 - 3:00] Code Walkthrough**
- *Visual*: Walk through the `tracker.py` and `download_video.py` scripts briefly.
- *Voiceover*: "The pipeline is built with modularity in mind. I created a script to automatically download a short cricket video using yt-dlp. In the main tracking script, I use OpenCV to read the video frame-by-frame, pass it to the YOLOv8 tracker, and then use the built-in plotting utilities to overlay bounding boxes and IDs before saving the final MP4."

**[3:00 - 4:00] Results Demonstration**
- *Visual*: Open the raw `input_video.mp4` for a few seconds, then switch to playing `output_tracked.mp4`. Pause the video occasionally to point out specific IDs.
- *Voiceover*: "Here is the raw input video, which is a short clip of a cricket match showing multiple players moving across the field. And here is the processed output. As you can see, each player is enclosed in a bounding box with a unique ID number. Notice how [point to an example in the video] when players cross paths or overlap slightly, the IDs remain stable. This shows ByteTrack effectively handling partial occlusions."

**[4:00 - 5:00] Challenges and Future Improvements**
- *Visual*: Keep the output video playing in the background, or switch to the `technical_report.md`.
- *Voiceover*: "Some of the main challenges observed were heavy occlusions and rapid camera panning, which can disrupt the linear motion predictions of the Kalman filter. If I were to improve this pipeline further, I would implement two things: first, Camera Motion Compensation to handle camera pans, and second, a visual Re-Identification model, like BoT-SORT, to remember jersey colors and appearances, which would help recover IDs after long-term occlusions. Thank you for watching."
