# contour detection
#   first convert image into 'L'
#   then, simply use a fixed threshold to extract edge
#   besides, to avoid heavy workload,
#       it will resize image to no more than 1000x1000
#
# input: location of image file
# output: image contour
#   a np.array of [(x,y),(x,y)....]
#    with shape of nx2
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import math


class ContourExtract():
    def __init__(self, image_path: str):
        self.img = Image.open(image_path).convert('L')

    def __resize(self):
        allowed_max = 1000
        rate = max(self.img.width / allowed_max, self.img.height / allowed_max)
        self.img = self.img.resize((math.floor(
            self.img.width / rate), math.floor(self.img.height / rate)),
                                   Image.ANTIALIAS)

    # randomly sample points to reduce workload
    def __sample(self):
        sample_rate = 0.1
        sample_max = 200
        idx = np.random.choice(len(self.points),
                               min(sample_max,
                                   math.floor(len(self.points) * sample_rate)),
                               replace=False)  # different number
        self.points = self.points[idx]

    def show(self):
        _, ax = plt.subplots()
        ax.scatter(self.points[:, 0], self.points[:, 1], s=1, alpha=0.5)
        plt.show()

    def extractImage(self) -> np.array:
        self.__resize()
        points = []
        threshold = 120
        img = np.array(self.img)
        for i in range(self.img.width):
            for j in range(self.img.height):
                if img[j, i] < threshold:
                    points.append([i, self.img.height - j - 1])

        self.points = np.array(points)
        print("{} points from image".format(len(self.points)))

        self.__sample()
        print("{} points after sample".format(len(self.points)))
        return self.points
