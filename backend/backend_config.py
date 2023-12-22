import torch
class config:
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    IN_CHANNELS = 128
    Z_DIM = 256
    ATTRIB_DIM = 17
    CHANNELS_IMG = 3