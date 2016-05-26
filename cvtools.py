import numpy as np
import os

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


def ipynb_show_matrix(matrix, title='', figsize=_DEFAULT_IMAGE_FIGSIZE):
  matrix_image = 255.0 * (matrix - np.min(matrix)) / (
      np.max(matrix) - np.min(matrix))
  ipynb_show_image(matrix_image, title, figsize)


def ipynb_show_color_histogram(histogram, plot_title=''):
  fig, ax = plt.subplots(figsize=(12, 1.5))
  ax.set_title(plot_title)
  ax.bar(range(len(histogram)), histogram, color='r', width=1)


class VideoReader(object):

  def __init__(self):
    self._clear()

  def _clear(self):
    self.video_file_path = None
    self.capture = None
    self.width = 0
    self.height = 0
    self.number_of_frames = 0
    self.frame_rate = 0.0
    self.current_frame_index = 0

  def is_opened(self):
    return self.video_file_path is not None and (
        self.capture is not None and self.capture.isOpened())

  def get_width(self):
    return self.width

  def get_height(self):
    return self.height

  def get_number_of_frames(self):
    return self.number_of_frames

  def get_frame_rate(self):
    return self.frame_rate

  def get_current_frame_index(self):
    return self.current_frame_index

  def open(self, video_file_path):
    self.video_file_path = video_file_path
    if not os.path.isfile(self.video_file_path):
      self._clear()
      raise IOError('cannot open video: <%s> is not a valid file' % video_file_path)

    self.capture = cv2.VideoCapture(self.video_file_path)
    if not self.is_opened():
      self._clear()
      raise IOError('cannot open video: <%s> is not a valid video file' % video_file_path)

    # Read video properites.
    self.width = int(self.capture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
    self.height = int(self.capture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
    self.number_of_frames = int(self.capture.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
    self.frame_rate = np.float32(self.capture.get(cv2.cv.CV_CAP_PROP_FPS))

  def get_frames(self):
    """
    Returns a video frame iterator.
    """
    while self.capture is not None:
      bln_frame_retrieved, frame = self.capture.read()
      if not bln_frame_retrieved:
        # Frame stream ended.
        raise StopIteration
      yield frame
      self.current_frame_index += 1
