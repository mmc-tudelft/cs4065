import cv2
import matplotlib.pyplot as plt

def ipynb_show_image(image):
  plt.imshow(image)
  plt.axis('off')


def ipynb_show_color_histogram(histogram, plot_title):
  fig, ax = plt.subplots(figsize=(12, 1.5))
  ax.set_title(plot_title)
  ax.bar(range(len(histogram)), histogram, color='r', width=1)
