import torch
from math import log2

START_TRAIN_AT_IMG_SIZE = 64
DATASET = 'celeb_dataset'
CHECKPOINT_GEN = "generator.pth"
CHECKPOINT_CRITIC = "critic.pth"
DEVICE =  "cuda" if torch.cuda.is_available() else "cpu"
SAVE_MODEL = True
LOAD_MODEL = True
LEARNING_RATE = 1e-3
BATCH_SIZES = [32, 32, 32, 16, 16, 16, 16, 8, 4]
CHANNELS_IMG = 3
Z_DIM = 256  # should be 512 in original paper
IN_CHANNELS = 128  # should be 512 in original paper
CRITIC_ITERATIONS = 1
LAMBDA_GP = 10
PROGRESSIVE_EPOCHS = [30] * len(BATCH_SIZES)
FIXED_NOISE = torch.full((8, Z_DIM, 1, 1),-1).to(DEVICE)
NUM_WORKERS = 2
ATTRIB_DIM = 17
FIXED_LABELS = torch.ones((8,ATTRIB_DIM)).to(DEVICE)