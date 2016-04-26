import types
import unittest

class TestLibrary(unittest.TestCase):

  def test_imports(self):
    try:
      import cv2
      import librosa
      import matplotlib
      import numpy
      import scipy
    except ImportError as e:
      self.fail(e)

  def test_opencv(self):
    try:
      import cv2
      self.assertTrue(type(cv2.SIFT) == types.BuiltinFunctionType)
    except AttributeError as e:
      self.fail(e)
    except ImportError as e:
      self.fail(e)

  def test_load_video(self):
    try:
      from datasets import CS4065_Dataset
      video_file_path = CS4065_Dataset.get_testcases_data()['video']
      # TODO(alessio): load and check properties (e.g., stream length).
      raise NotImplementedError()
    except ImportError as e:
      self.fail(e)

  def test_load_audio(self):
    try:
      from datasets import CS4065_Dataset
      audio_file_path = CS4065_Dataset.get_testcases_data()['audio']
      # TODO(alessio): check properties (e.g., stream length).
      raise NotImplementedError()
    except ImportError as e:
      self.fail(e)

  def test_load_image(self):
    try:
      import cv2
      import numpy as np
      from datasets import CS4065_Dataset
      image_file_path = CS4065_Dataset.get_testcases_data()['image']
      image = cv2.imread(image_file_path)
      self.assertTrue((512, 512, 3) == np.shape(image))
    except ImportError as e:
      self.fail(e)

if __name__ == "__main__":
  unittest.main()
