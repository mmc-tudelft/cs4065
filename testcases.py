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
      import numpy as np

      from datasets import CS4065_Dataset
      from cvtools import VideoReader

      video_file_path = CS4065_Dataset.get_testcases_data()['video']

      video_reader = VideoReader()
      video_reader.open(video_file_path)

      video_width = video_reader.get_width()
      video_height = video_reader.get_height()
      number_of_frames = video_reader.get_number_of_frames()
      frame_rate = video_reader.get_frame_rate()

      self.assertTrue(video_reader.is_opened())
      self.assertTrue(video_width > 0)
      self.assertTrue(video_height > 0)
      self.assertTrue(number_of_frames > 0)
      self.assertTrue(video_reader.get_frame_rate() > 0)

      read_frames = 0
      for frame in video_reader.get_frames():
        frame_shape = np.shape(frame)
        self.assertEqual(read_frames, video_reader.get_current_frame_index())
        self.assertEqual(len(frame_shape), 3)
        self.assertEqual(frame_shape[0], video_height)
        self.assertEqual(frame_shape[1], video_width)
        read_frames += 1

      # No bit exactness, allow 1/5 second of lenght difference.
      length_tolerance = int(np.round(frame_rate / 5.0))
      self.assertLessEqual(np.abs(read_frames - number_of_frames), length_tolerance)
    except ImportError as e:
      self.fail(e)
    except IOError as e:
      self.fail(e)

  def test_load_audio(self):
    try:
      import numpy as np
      import librosa
      from datasets import CS4065_Dataset

      audio_file_path = CS4065_Dataset.get_testcases_data()['audio']
      y, sample_rate = librosa.core.load(audio_file_path)

      self.assertEqual(sample_rate, 22050)

      # Mono signal expected.
      y_shape = np.shape(y)
      self.assertEqual(len(y_shape), 1)

      # No bit exactness, allow 1/5 second of lenght difference.
      length_tolerance = int(np.round(float(sample_rate) / 5.0))
      self.assertLessEqual(np.abs(y_shape[0] - 37309), length_tolerance)
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

  def test_wraprec(self):
    try:
      from wraprec import PyWrapRec
      PyWrapRec.check_dependencies()
    except ImportError as e:
      self.fail(e)
    except IOError as e:
      self.fail(e)

if __name__ == "__main__":
  unittest.main()
