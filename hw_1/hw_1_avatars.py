import os
from PIL import Image
import numpy as np
from collections import defaultdict
from pathlib import Path

class AvatarGenerator():
    def __init__(self, avatars_path):
        self.avatars_path = avatars_path
        self.pixel_counts = defaultdict(lambda: np.zeros((256, 4)))
        self.pixel_probs = {}
        self.img_size = 0, 0, 0
        self.get_pixel_probs()

    def get_pixel_probs(self):
        total_images = 0
        for image_path in os.listdir(self.avatars_path):

            img = Image.open(f'{self.avatars_path}/{image_path}')
            img_arr = np.array(img)
            self.img_size = img_arr.shape
            height, width, channels = img_arr.shape

            for i in range(height):
                for j in range(width):
                    for channel in range(channels):
                        intensity = img_arr[i, j, channel]
                        self.pixel_counts[(i, j)][intensity, channel] += 1

            total_images += 1

        for pos in self.pixel_counts:
            actual_channels = 4 if np.sum(self.pixel_counts[pos][:, 3]) > 0 else 3

            mle_probs = np.zeros((256, 4))
            bayes_probs = np.zeros((256, 4))

            for channel in range(actual_channels):
                mle_probs[:, channel] = self.pixel_counts[pos][:, channel] / total_images
                bayes_probs[:, channel] = (self.pixel_counts[pos][:, channel] + 1) / (total_images + 256)

            self.pixel_probs[pos] = {
                'mle': mle_probs,
                'bayes': bayes_probs
            }

    def generate_avatar(self, avatar_path, method='bayes'):
        height, width = self.img_size[0], self.img_size[1]
        channels = 4 if any(np.sum(self.pixel_counts[pos][:, 3]) > 0 for pos in self.pixel_counts) else 3
        new_img = np.zeros((height, width, channels), dtype=np.uint8)

        for i in range(height):
            for j in range(width):
                pos = (i, j)
                probs = self.pixel_probs[pos][method]
                for channel in range(channels):
                    intensities = np.arange(256)
                    channel_probs = probs[:, channel]
                    channel_probs = channel_probs / channel_probs.sum()
                    np.random.seed()
                    intensity = np.random.choice(intensities, p=channel_probs)
                    new_img[i, j, channel] = intensity

        img = Image.fromarray(new_img)
        img.save(avatar_path)


if __name__ == '__main__':

    root_dir = Path(__file__).resolve().parent
    generator = AvatarGenerator(os.path.join(root_dir, 'avatars'))

    n = 2
    for i in range(1, n+1):
        generator.generate_avatar(os.path.join(root_dir, f'test_avatar_bayes{i}.png'))
