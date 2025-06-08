# Video Processing Tool

A Python-based video processing tool that allows you to enhance and modify videos using super-resolution and other features.

## Features

### Super Resolution
- Upscale video resolution using ESRT (Efficient Super Resolution Transformer) model
- Supports 2x, 3x, and 4x upscaling
- Maintains original video FPS
- Processes videos frame by frame for high-quality results

### Video Processing Options
- Change video resolution
- Modify frame rate (FPS)
- Trim video (start time and duration)
- Adjust playback speed
- Maintain original video quality when no changes are specified

## Requirements

```bash
pip install -r requirements.txt
```

Required packages:
- torch>=2.0.0
- torchvision>=0.15.0
- opencv-python>=4.8.0
- numpy>=1.24.0

## Usage

1. Run the application:
```bash
python main.py
```

2. In the GUI:
   - Select your input video file
   - Choose processing options:
     - FPS: Enter new frame rate or leave as "no change"
     - Width/Height: Enter new dimensions or leave as "no change"
     - Start Time: Enter trim start point in seconds
     - Duration: Enter trim duration in seconds
     - Speed: Enter playback speed multiplier
     - Super Resolution: Select upscaling factor (x2, x3, x4)

3. Click "Process" to start video processing

## Model Weights

The super-resolution model requires pre-trained weights. Place the model weights in the `weights` directory:
- `ESRT_x2.pth` for 2x upscaling
- `ESRT_x3.pth` for 3x upscaling
- `ESRT_x4.pth` for 4x upscaling


<img width="609" alt="Screenshot 2025-01-23 at 7 05 44 PM" src="https://github.com/user-attachments/assets/084f73e1-1bee-4b62-945e-57c3a32b90d1" />


