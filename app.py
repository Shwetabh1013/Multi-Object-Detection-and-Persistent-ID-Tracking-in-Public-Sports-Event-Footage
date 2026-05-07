import gradio as gr
import os
import subprocess
from tracker import run_tracking

def process_video(input_video_path):
    if input_video_path is None:
        return None
    
    temp_output_path = "temp_output.mp4"
    final_output_path = "final_output.mp4"
    
    print(f"Running tracking on {input_video_path}...")
    run_tracking(input_video_path, temp_output_path)
    
    print("Converting to libx264 for web compatibility...")
    if os.path.exists(final_output_path):
        os.remove(final_output_path)
        
    cmd = ["ffmpeg", "-y", "-i", temp_output_path, "-vcodec", "libx264", "-preset", "fast", "-crf", "28", final_output_path]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return final_output_path
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"FFmpeg conversion failed: {e}")
        return temp_output_path

iface = gr.Interface(
    fn=process_video,
    inputs=gr.Video(label="Upload Sports Video"),
    outputs=gr.Video(label="Tracked Output Video"),
    title="Multi-Object Sports Tracking",
    description="Upload a video to see YOLOv8 + ByteTrack in action, identifying and tracking multiple subjects persistently."
)

if __name__ == "__main__":
    iface.launch(share=True)
