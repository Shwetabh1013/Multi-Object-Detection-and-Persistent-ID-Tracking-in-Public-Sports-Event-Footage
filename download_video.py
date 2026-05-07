import os
import yt_dlp

def download_sample_video():
    """
    Downloads a short sample cricket video using yt-dlp.
    """
    video_filename = "input_video.mp4"
    
    if os.path.exists(video_filename):
        print(f"{video_filename} already exists. Skipping download.")
        return

    print("Downloading sample cricket video...")
    
    ydl_opts = {
        'format': 'best[ext=mp4]',
        'outtmpl': 'input_video.%(ext)s',
        'noplaylist': True,
        'max_downloads': 1
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(['ytsearch1:cricket match short'])
    except Exception as e:
        if os.path.exists(video_filename):
            pass 
        else:
            print(f"Error downloading video: {e}")
            return
            
    print(f"Successfully downloaded {video_filename}")

if __name__ == "__main__":
    download_sample_video()
