import subprocess
from datetime import datetime
from sr import SuperResolution
import os
import cv2

class VideoProcessor:

    def __init__(self, input, fps, start_time, duration, height, width, speed, sr_factor="no change"):
        # Get original video FPS
        cap = cv2.VideoCapture(input)
        original_fps = cap.get(cv2.CAP_PROP_FPS)
        cap.release()
        
        self.metadata = {
            "input": input, 
            "fps": fps if fps != -1 else original_fps,  # Use original FPS if no change specified
            "start_time": start_time, 
            "duration": duration,
            "height": height, 
            "width": width, 
            "speed": speed,
            "sr_factor": sr_factor
        }
        self.sr_processor = None
        if sr_factor != "no change":
            self.sr_processor = SuperResolution(upscale_factor=int(sr_factor[1:]))

    def convert_seconds(self, seconds):
        hours = seconds // 3600               # Calculate hours
        minutes = (seconds % 3600) // 60      # Calculate remaining minutes
        remaining_seconds = seconds % 60      # Calculate remaining seconds
        return hours, minutes, remaining_seconds

    def finalise_ffmpeg_command(self):
        open_quotes, close_quotes = 0, 0
        input_name = self.metadata["input"].split(".mp4")
        date_time = datetime.now().strftime("%d%m%Y_%H%M%S")
        output_name = f"{input_name[0]}_{date_time}"
        
        # If super resolution is selected, process the video first
        if self.sr_processor:
            sr_output = f"{output_name}_sr.mp4"
            self.sr_processor.process_video(
                self.metadata["input"],
                sr_output,
                self.metadata["fps"]  # Now using the correct FPS (original or specified)
            )
            # Update input to the super-resolved video
            self.metadata["input"] = sr_output
            output_name = f"{output_name}_processed"

        # print(output_name)
        # cmd = f'ffmpeg -i "{self.metadata["input"]}" -y '

        # if self.metadata["start_time"] != -1:
        #     h, m, s = self.convert_seconds(int(self.metadata["start_time"]))
        #     cmd += f'-ss {h}:{m}:{s} '            
        # if self.metadata["duration"] != -1:
        #     cmd += f'-t {self.metadata["duration"]} ' 
        # if self.metadata["fps"] != -1:
        #     open_quotes = 1
        #     cmd += f'-vf "fps={self.metadata["fps"]} '
        # if self.metadata["width"] != -1 or self.metadata["height"] != -1:
        #     if open_quotes:
        #         cmd += f', scale={self.metadata["width"]}:{self.metadata["height"]} '
        #     else:
        #         open_quotes = 1 
        #         cmd += f'-vf "scale={self.metadata["width"]}:{self.metadata["height"]} '
        # if self.metadata["speed"] != -1 and self.metadata["speed"] != "no change":
        #     if open_quotes:
        #         cmd += f', setpts={round(1/float(self.metadata["speed"]), 1)}*PTS" -filter:a "atempo={self.metadata["speed"]}"'
        #     else:
        #         cmd += f'-vf "setpts={round(1/float(self.metadata["speed"]), 1)}*PTS" -filter:a "atempo={self.metadata["speed"]}"' 
        #     close_quotes = 1
        
        # if open_quotes and not close_quotes:  
        #     cmd += f'\" {output_name}.mp4'
        # else:
        #     cmd += f' {output_name}.mp4'
        
        # print(f"processing video {cmd}")
    
        # p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        # p.wait()

        # # Clean up temporary super-resolved video if it exists
        # if self.sr_processor and os.path.exists(sr_output):
        #     os.remove(sr_output)

        return "video processed complete"
