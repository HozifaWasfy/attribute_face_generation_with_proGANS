# Conditional Pro GANs for Face Generation

## Overview

This repository contains the implementation of conditional Progressive GANs (Generative Adversarial Networks) for face generation. The model allows the generation of synthetic faces with specific attributes controlled during the training process.

## Features

- **Conditional Generation:** The model supports conditional face generation, allowing the control of various facial attributes such as age, gender and various face features.

- **Progressive Training:** Utilizes a progressive training approach to generate high-resolution faces in a step-by-step manner.

- **Pytorch Implementation:** Implemented using PyTorch, a popular deep learning framework.

## Getting Started

### Prerequisites

- Python 3
- PyTorch
- see requirments.txt


### Installation

1. Clone this repository:
   ```bash
   git clone this repo
   cd attribute_face_generation_with_proGANS
2. Download the pretrained weights from [generator](https://drive.google.com/file/d/1eR83o8quD2WBF3vHGfPqyLjF9YuDHp4m/view?usp=sharing), [discriminator](https://drive.google.com/file/d/1uuay6YHTibvdkBh7LBiDX064gWKrC5F1/view?usp=sharing)
3. Explore the model with the test jupyter notebook
