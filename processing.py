import subprocess
from datetime import datetime

class VideoProcessor:

    def __init__(self, input, fps, start_time, duration, height, width, speed):
        self.metadata = {"input": input, "fps": fps, "start_time": start_time, "duration": duration,
                          "height": height, "width": width, "speed": speed}

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
        print(output_name)
        cmd = f'ffmpeg -i {self.metadata["input"]} -y '

        if self.metadata["start_time"] != -1:
            h, m, s = self.convert_seconds(int(self.metadata["start_time"]))
            cmd += f'-ss {h}:{m}:{s} '            
        if self.metadata["duration"] != -1:
            cmd += f'-t {self.metadata["duration"]} ' 
        if self.metadata["fps"] != -1:
            open_quotes = 1
            cmd += f'-vf "fps={self.metadata["fps"]} '
        if self.metadata["width"] != -1 or self.metadata["height"] != -1:
            if open_quotes:
                cmd += f', scale={self.metadata["width"]}:{self.metadata["height"]} '
            else:
                open_quotes = 1 
                cmd += f'-vf "scale={self.metadata["width"]}:{self.metadata["height"]} '
        if self.metadata["speed"] != -1:
            if open_quotes:
                cmd += f', setpts={round(1/float(self.metadata["speed"]), 1)}*PTS" -filter:a "atempo={self.metadata["speed"]}"'
            else:
                cmd += f'-vf "setpts={round(1/float(self.metadata["speed"]), 1)}*PTS" -filter:a "atempo={self.metadata["speed"]}"' 
            close_quotes = 1
        
        if open_quotes and not close_quotes:  
            cmd += f'\" {output_name}.mp4'
        else:
            cmd += f' {output_name}.mp4'
        
        print(f"processing video {cmd}")
    
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        p.wait()
        return "video processed complete"
