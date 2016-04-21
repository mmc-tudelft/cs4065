import numpy as np

import cv2
import matplotlib.pyplot as plt

_DEFAULT_IMAGE_FIGSIZE = (7, 7)

def ipynb_show_cv2_image(image_bgr, title='', figsize=_DEFAULT_IMAGE_FIGSIZE):
  image_rgb = image_bgr.copy()
  image_rgb[:, :, 0] = image_bgr[:, :, 2]
  image_rgb[:, :, 2] = image_bgr[:, :, 0]
  ipynb_show_image(image_rgb, title, figsize)


def ipynb_show_image(image, title='', figsize=_DEFAULT_IMAGE_FIGSIZE):
  fig, ax = plt.subplots(figsize=figsize)
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
