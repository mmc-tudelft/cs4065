import numpy as np

import cv2
import matplotlib.pyplot as plt

def ipynb_show_image(image, title=''):
  fig, ax = plt.subplots(figsize=(7, 7))
  ax.set_title(title)
  plt.imshow(image)
  plt.axis('off')


def ipynb_show_matrix(matrix, title=''):
  matrix_image = 255.0 * (matrix - np.min(matrix)) / (
      np.max(matrix) - np.min(matrix))
  ipynb_show_image(matrix_image, title)


def ipynb_show_color_histogram(histogram, plot_title=''):
  fig, ax = plt.subplots(figsize=(12, 1.5))
  ax.set_title(plot_title)
  ax.bar(range(len(histogram)), histogram, color='r', width=1)
