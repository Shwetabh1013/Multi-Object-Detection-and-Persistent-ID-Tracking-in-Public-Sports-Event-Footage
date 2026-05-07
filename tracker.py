import cv2
from ultralytics import YOLO
import argparse
import os

def run_tracking(input_video_path, output_video_path):
    print("Loading YOLOv8 model...")
    model = YOLO('yolov8s.pt')
    
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video {input_video_path}")
        return
        
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(f"Video Properties: {width}x{height} @ {fps}fps, {total_frames} frames total")
    
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
    
    frame_count = 0
    print(f"Starting multi-object tracking...")
    
    
    results = model.track(
        source=input_video_path,
        conf=0.3,         
        iou=0.5,          
        show=False,       
        tracker="bytetrack.yaml", 
        classes=[0, 32],      
        stream=True       
    )
    
    for r in results:
        frame_count += 1
        
        annotated_frame = r.plot()
        
        out.write(annotated_frame)
        
        if frame_count % 30 == 0:
            print(f"Processed {frame_count}/{total_frames} frames...")
            
    cap.release()
    out.release()
    print(f"Tracking complete. Output saved to {output_video_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-Object Tracking using YOLOv8")
    parser.add_argument("--input", type=str, default="input_video.mp4", help="Path to input video")
    parser.add_argument("--output", type=str, default="output_tracked.mp4", help="Path to output video")
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"Error: Input video '{args.input}' not found. Please run download_video.py first.")
    else:
        run_tracking(args.input, args.output)
