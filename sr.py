import torch
import cv2
import numpy as np
import os
from model import esrt
import utils

class SuperResolution:
    def __init__(self, upscale_factor=2):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.upscale_factor = upscale_factor
        self.model = self.load_model()

    def load_model(self):
        model = esrt.ESRT(upscale=self.upscale_factor)
        model_path = os.path.join('weights', f'ESRT_x{self.upscale_factor}.pth')
        model_dict = utils.load_state_dict(model_path)
        model.load_state_dict(model_dict, strict=False)
        model = model.to(self.device)
        model.eval()
        return model

    def process_frame(self, frame):
        # Convert BGR to RGB
        frame = frame[:, :, [2, 1, 0]]
        
        # Normalize and convert to tensor
        im_input = frame / 255.0
        im_input = np.transpose(im_input, (2, 0, 1))
        im_input = im_input[np.newaxis, ...]
        im_input = torch.from_numpy(im_input).float()
        
        # Move to device
        im_input = im_input.to(self.device)
        
        # Process frame
        with torch.no_grad():
            out = self.model(im_input)
        
        # Convert back to numpy
        out_img = utils.tensor2np(out.detach()[0])
        
        # Convert RGB to BGR for OpenCV
        out_img = out_img[:, :, [2, 1, 0]]
        
        return out_img

    def process_video(self, input_path, output_path, fps):
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            raise ValueError("Could not open input video")

        # Get video properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Calculate new dimensions after super resolution
        new_width = width * self.upscale_factor
        new_height = height * self.upscale_factor

        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (new_width, new_height))

        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Process frame
            processed_frame = self.process_frame(frame)
            out.write(processed_frame)
            
            frame_count += 1
            if frame_count % 10 == 0:
                print(f"Processed {frame_count} frames")

        cap.release()
        out.release()
        return True 