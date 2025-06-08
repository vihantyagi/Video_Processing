from UI import GUI
from processing import VideoProcessor


def handle_processing(data):
    input, start_time, duration, fps, width, height, speed, sr_factor = data
    processing_obj = VideoProcessor(input, fps, start_time, duration, height, width, speed, sr_factor)
    print(processing_obj.finalise_ffmpeg_command())
    return True

gui_obj = GUI()
gui_obj.set_callback(handle_processing)
gui_obj.execute_main()
