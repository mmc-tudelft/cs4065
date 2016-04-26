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

