import os

from config import PATH_DATA

class CS4065_Dataset(object):
  def __init__(self):
    pass

  @classmethod
  def get_poster_images(cls):
    images = []
    path_to_images = os.path.join(PATH_DATA, 'poster_images')
    for image_filename in os.listdir(path_to_images):
      image_filepath = os.path.join(path_to_images, image_filename)
      if not os.path.isfile(image_filepath):
        continue
      images.append(image_filepath)
    return images
