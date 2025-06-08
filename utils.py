import numpy as np
import torch
from collections import OrderedDict

def tensor2np(tensor, out_type=np.uint8, min_max=(0, 1)):
    tensor = tensor.float().cpu().clamp_(*min_max)
    tensor = (tensor - min_max[0]) / (min_max[1] - min_max[0])  # to range [0, 1]
    img_np = tensor.numpy()
    img_np = np.transpose(img_np, (1, 2, 0))
    if out_type == np.uint8:
        img_np = (img_np * 255.0).round()
    return img_np.astype(out_type)

def load_state_dict(path):
    # Load weights to CPU by default
    state_dict = torch.load(path, map_location=torch.device('cpu'))
    new_state_dict = OrderedDict()
    for k, v in state_dict.items():
        if 'module' in k:
            name = k[7:]  # remove 'module.' prefix
        else:
            name = k
        new_state_dict[name] = v
    return new_state_dict