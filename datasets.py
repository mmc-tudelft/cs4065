import os
import shutil
import tarfile
import urllib

from config import PATH_DATA

class CS4065_Dataset(object):

  DATASET_ARCHIVE_URLS = {
      'poster_images': None,
      'testcases': 'https://www.dropbox.com/s/z7nenlpkrcsodrt/testcases.tar.gz?dl=1',
  }

  def __init__(self):
    pass

  @classmethod
  def get_poster_images(cls):
    path_to_images = cls._get_dataset_path('poster_images')

    images = []
    for image_filename in os.listdir(path_to_images):
      image_filepath = os.path.join(path_to_images, image_filename)
      if not os.path.isfile(image_filepath):
        continue
      images.append(image_filepath)

    return images

  @classmethod
  def get_testcases_data(cls):
    path = cls._get_dataset_path('testcases')
    return {
        'audio': os.path.join(path, 'castagnettes.mp3'),
        'image': os.path.join(path, 'lena.jpg'),
        'video': os.path.join(path, 'big_buck_bunny.mp4'),
    }

  @classmethod
  def _get_dataset_path(cls, dataset_name):
    # Check that the dataset name is valid.
    assert dataset_name in cls.DATASET_ARCHIVE_URLS

    # Fetch the dataset if not deployed.
    path = os.path.join(PATH_DATA, dataset_name)
    if not os.path.exists(path):
      # Check if the dataset can be fetched.
      if cls.DATASET_ARCHIVE_URLS[dataset_name] is None:
        raise IOError('The <%s> dataset should be manually feteched.' % dataset_name)

      # Fetch dataset.
      try:
        print '[notice] fetching <%s> dataset' % dataset_name
        cls._fetch_dataset(cls.DATASET_ARCHIVE_URLS[dataset_name], path)
      except Exception as e:
        print '[error] cannot fetch <%s> dataset (%s)' % (dataset_name, e)
        # Remove content in the dataset folder.
        try:
          shutil.rmtree(path)
        except:
          pass

    # Dataset deployed and ready for use.
    return path

  @classmethod
  def _fetch_dataset(cls, url, dataset_path):
    os.mkdir(dataset_path)
    (temp_file_path, headers) = urllib.urlretrieve(url)
    tar_file = tarfile.open(temp_file_path, 'r:gz')
    tar_file.extractall(dataset_path)
