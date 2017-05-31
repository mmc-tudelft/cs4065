import os
import shutil
import tarfile
import urllib
import pickle
import subprocess
import tempfile
import zipfile

from config import PATH_DATA

class CS4065_Dataset(object):

  DATASET_ARCHIVE_URLS = {
      'poster_images': None,
      'testcases': 'https://www.dropbox.com/s/z7nenlpkrcsodrt/testcases.tar.gz?dl=1',
      'movielens_subset': 'https://www.dropbox.com/s/mbzgntv787x75ld/movielens_subset.tar.gz?dl=1',
      'wraprec_sample_data3': 'https://www.dropbox.com/s/j46m8qdbkh3vtb3/wraprec_sample_data.tar.gz?dl=1',
      'songretrieval_subset': 'https://www.dropbox.com/s/wubrlxput9cstn1/songretrieval-small.tar.gz?dl=1',
      'songretrieval_queries': 'https://www.dropbox.com/s/km4zcqagvi7i5rk/songretrieval-queries.tar.gz?dl=1',
      'msra_mm1_subset': 'https://www.dropbox.com/s/bfj2wx50rapxnlz/msra-mm1_subset.tar.gz?dl=1',
      'vgg19_model': 'https://s3.amazonaws.com/lasagne/recipes/pretrained/imagenet/vgg19.pkl',
      'vse_model': 'http://www.cs.toronto.edu/~rkiros/models/vse.zip',
  }

  def __init__(self):
    pass

  @classmethod
  def get_wraprec_sample_data(cls):
    """
    It returns the path to the configuration file for the WrapRec toolbox.
    """
    path_to_files = cls._get_dataset_path('wraprec_sample_data3')
    config_file_path = os.path.join(path_to_files, 'sample.xml')
    assert os.path.exists(config_file_path)
    return config_file_path

  @classmethod
  def get_movielens_subset(cls):
    path_to_files = cls._get_dataset_path('movielens_subset')

    path_to_file_dict = {}

    for rating_data_path in os.listdir(path_to_files):
      full_filepath = os.path.join(path_to_files, rating_data_path)
      if os.path.isfile(full_filepath):
        path_to_file_dict[rating_data_path] = full_filepath

    return path_to_file_dict

  @classmethod
  def get_msra_mm1_subset(cls):
    path_to_root = cls._get_dataset_path('msra_mm1_subset')
    image_prefix = os.path.join(path_to_root, 'msra-mm1_subset/Images')
    features_prefix = os.path.join(path_to_root, 'msra-mm1_subset/Features')

    msra_mm1_data = {}

    for category_data_path in os.listdir(features_prefix):
      if not category_data_path.startswith('.'):
        category = category_data_path[:-4]
        full_category_data_path = os.path.join(features_prefix, category_data_path)
        category_data = pickle.load(open(full_category_data_path, 'rb'))

        full_image_paths = []

        for original_rank in category_data['original_ranks']:
          full_image_paths.append(os.path.join(image_prefix, '%s/%s.jpg' % (category, original_rank)))

        category_data['image_paths'] = full_image_paths

        msra_mm1_data[category] = category_data

    return msra_mm1_data

  @classmethod
  def get_songretrieval_subset(cls):
    path_to_files = cls._get_dataset_path('songretrieval_subset')

    path_to_file_dict = {}

    for mp3_file_path in os.listdir(path_to_files):
      if not mp3_file_path.endswith('.mp3'):
        continue
      full_filepath = os.path.join(path_to_files, mp3_file_path)
      if os.path.isfile(full_filepath):
        path_to_file_dict[mp3_file_path] = full_filepath

    return path_to_file_dict

  @classmethod
  def get_songretrieval_queries(cls):
    path_to_files = cls._get_dataset_path('songretrieval_queries')

    path_to_file_dict = {}

    for mp3_file_path in os.listdir(path_to_files):
      if not mp3_file_path.endswith('.mp3'):
        continue
      full_filepath = os.path.join(path_to_files, mp3_file_path)
      if os.path.isfile(full_filepath):
        path_to_file_dict[mp3_file_path] = full_filepath

    return path_to_file_dict

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
  def get_vse_models(cls):
    """
    Since their model has different file configuration,
    this method is implemented as in adhoc manner
    """
    url_to_vgg = cls.DATASET_ARCHIVE_URLS['vgg19_model']
    url_to_vse = cls.DATASET_ARCHIVE_URLS['vse_model']

    path_to_vgg = os.path.join(PATH_DATA,'vgg19_model')
    path_to_vse = os.path.join(PATH_DATA,'vse_model')

    vgg_fn = os.path.join(path_to_vgg,'vgg19.pkl')
    if not os.path.exists(vgg_fn):
        if not os.path.exists(path_to_vgg):
            os.makedirs(path_to_vgg)

        # download each model with wget
        subprocess.call(['wget',url_to_vgg])
        os.rename(
            os.path.join(os.getcwd(),'vgg19.pkl'),
            os.path.join(path_to_vgg,'vgg19.pkl')
        )

    vse_fn = os.path.join(path_to_vse,'coco.npz')
    if not os.path.exists(vse_fn):

        if not os.path.exists(path_to_vse):
            os.makedirs(path_to_vse)

        # unzip vse model (.zip file)
        subprocess.call(['wget',url_to_vse])
        zip_path = os.path.join(os.getcwd(),'vse.zip')
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            zipf.extractall(path_to_vse)

        # delete zip file
        os.remove(zip_path)

    return {
        'vgg19_model':vgg_fn,
        'vse_model':vse_fn
    }

  @classmethod
  def get_coco_testset(cls):
    import urllib2

    src = "http://www.cs.toronto.edu/~rkiros/vse_coco_dev.html"
    response = urllib2.urlopen(src)
    x = response.readlines()

    # get important lines
    Y = [(x[j+1],x[j+4]) for j in xrange(39,len(x)-9,9)]

    # parse strings
    im_root = 'http://www.cs.toronto.edu/~rkiros/'
    Z = map(
        lambda y:
        (
            im_root + y[0].split('src="')[-1].split('"><')[0][2:],
            y[1].split('<br>')[-1].replace('\n','')
        ),
        Y
    )

    return Z

  @classmethod
  def _get_dataset_path(cls, dataset_name):
    # Check that the dataset name is valid.
    assert dataset_name in cls.DATASET_ARCHIVE_URLS

    # Fetch the dataset if not deployed.
    path = os.path.join(PATH_DATA, dataset_name)
    if not os.path.exists(path):
      # Check if the dataset can be fetched.
      if cls.DATASET_ARCHIVE_URLS[dataset_name] is None:
        raise IOError('The <%s> dataset should be manually fetched.' % dataset_name)

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
    os.makedirs(dataset_path)
    (temp_file_path, headers) = urllib.urlretrieve(url)
    tar_file = tarfile.open(temp_file_path, 'r:gz')
    tar_file.extractall(dataset_path)
