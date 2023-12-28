import unittest
import torch
import sys 
from math import log2
sys.path.append("..")
from models.model import Generator, Discriminator


class TestModels(unittest.TestCase):

    def setUp(self):
        self.ATTRIB_DIM = 10
        self.Z_DIM = 256
        self.IN_CHANNELS = 256
        self.img_channels = 3
        self.get_step = lambda img_size: int(log2(img_size / 4))
        self.Z = lambda batch_size: torch.randn((batch_size, self.Z_DIM, 1, 1))
        self.Labels =lambda batch_size: torch.full((batch_size, self.ATTRIB_DIM), -1, dtype=torch.float32)
        self.img_sizes = [4, 8, 16, 32, 64, 128, 256, 512, 1024]
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.critic = Discriminator(self.Z_DIM, self.IN_CHANNELS, 10, img_channels=3).to(self.device)
        self.gen = Generator(self.Z_DIM, self.IN_CHANNELS,10, img_channels=3).to(self.device)

    def test_generator_forward(self):
        # Test the forward pass of the generator
        batch_size = 2
        z = self.Z(batch_size).to(self.device)
        labels = self.Labels(batch_size).to(self.device)
        alpha = 0.5
        for img_size in self.img_sizes:
            steps = self.get_step(img_size)  # Adjust the value based on your model architecture
            generated_images = self.gen(z, labels, alpha, steps)
            self.assertEqual(generated_images.shape, (batch_size, self.img_channels, img_size, img_size))

    def test_discriminator_forward(self):
        # Test the forward pass of the discriminator
        batch_size = 16
        for img_size in self.img_sizes:
            real_images = torch.randn((batch_size, self.img_channels, img_size, img_size)).to(self.device)  # Adjust the size based on your model
            labels = self.Labels(batch_size).to(self.device)
            alpha = 0.5
            steps = self.get_step(img_size)  # Adjust the value based on your model architecture

            fake_images = self.gen(self.Z(batch_size).to(self.device), labels, alpha, steps)
            real_logits = self.critic(real_images, labels, alpha, steps)
            fake_logits = self.critic(fake_images, labels, alpha, steps)

            self.assertEqual(real_logits.shape, (batch_size, 1))
            self.assertEqual(fake_logits.shape, (batch_size, 1))

    # Add more tests as needed

if __name__ == '__main__':
    unittest.main()
