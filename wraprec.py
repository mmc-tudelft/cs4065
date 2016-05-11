import os
import platform
import shutil
import subprocess
import sys
import tarfile
import urllib
from xml.etree import ElementTree

import pandas

from config import BASE_PATH

UNIX_INSTALL_MONO = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          'install_mono.sh')

WRAPREC_PATH = os.path.join(BASE_PATH, 'wraprec')

WRAPREC_BIN = os.path.join(WRAPREC_PATH, 'WrapRec.exe')

WRAPREC_VERSION_TAG_PATH = os.path.join(WRAPREC_PATH, 'VERSION.txt')

WRAPREC_VERSION = '2.0.4'

WRAPREC_URL = ('https://github.com/babakx/WrapRec/releases/download/{0}/'
               'wraprec.{0}.tar.gz'.format(WRAPREC_VERSION))

PLATFORM = platform.system()

class PyWrapRec(object):

  def __init__(self):
    raise Exception('Cannot instantiate. Call PyWrapRec.run(config_file_path) '
                    'as static method.')

  @classmethod
  def run(cls, config_file_path):
    """
    TODO(alessio): write inline doc
    """
    cls.check_dependencies()
    try:
      # WrapRec working directory (the same as the configuration file).
      wraprec_working_dir = os.path.dirname(config_file_path)

      # Build arguments list.
      args = cls._get_command() + [config_file_path]

      # Create a new process.
      process = subprocess.Popen(args, cwd=WRAPREC_PATH, bufsize=4096)
      exit_code = process.wait()

      if exit_code != 0:
        raise Exception('WrapRec error (exit code: %d)' % exit_code)

      return cls._parse_wraprec_reults(config_file_path)
    except subprocess.CalledProcessError as e:
      raise e

  @classmethod
  def check_dependencies(cls):
    if not cls._is_wraprec_deployed():
      cls._deploy_wraprec()
    cls._test_wraprec()

  @classmethod
  def _parse_wraprec_reults(cls, config_file_path):
    """
    Parse the WrapRec results.

    Args:
      config_file_path

    Returns:
      pandas.core.frame.DataFrame, pandas.core.frame.DataFrame
    """
    # Read experiment id and path to results from the configuration file.
    xml_config_file_root = cls._parse_wraprec_config_file(config_file_path)
    xml_experiments_node = xml_config_file_root.find('experiments')
    experiment_id = xml_experiments_node.get('run')
    results_path = xml_experiments_node.get('resultsFolder')
    csv_sep_char = xml_experiments_node.get('separator')
    if experiment_id is None or results_path is None:
      raise Exception('cannot parse WrapRec configuration file')

    # Find the output files to be parsed.
    results_file_path = os.path.join(results_path, '%s.csv' % experiment_id)
    splits_file_path = os.path.join(results_path, '%s.splits.csv' % (
        experiment_id))
    if not all([os.path.isfile(path) for path in [
        results_file_path, splits_file_path]]):
      raise Exception('cannot find WrapRec output files')

    # Parse output files with libpandas.
    results = pandas.read_csv(results_file_path, sep=csv_sep_char)
    split_info = pandas.read_csv(splits_file_path, sep=csv_sep_char)

    return results, split_info

  @classmethod
  def _parse_wraprec_config_file(cls, config_file_path):
    xml_tree = ElementTree.parse(config_file_path)
    return xml_tree.getroot()

  @classmethod
  def _test_wraprec(cls):
    try:
      args = cls._get_command()
      output = subprocess.check_output(args)
      if not output.startswith('WrapRec 2.0 recommendation toolkit.'):
        raise subprocess.CalledProcessError('Unexpected output.')
    except subprocess.CalledProcessError as e:
      raise e

  @classmethod
  def _get_command(cls):
    return [WRAPREC_BIN] if PLATFORM == 'Windows' else [
        'mono', WRAPREC_BIN]

  @classmethod
  def _is_wraprec_deployed(cls):
    if not os.path.exists(WRAPREC_BIN):
      return False

    # Check version.
    if not os.path.exists(WRAPREC_VERSION_TAG_PATH):
      return False
    with open(WRAPREC_VERSION_TAG_PATH) as f:
      return f.readline().strip() == WRAPREC_VERSION

  @classmethod
  def _deploy_wraprec(cls):
    print '[notice] deploying WrapRec'

    try:
      # Platform specific steps.
      if PLATFORM != 'Windows':
        print '[notice] installing mono for Unix'
        cls._install_mono_unix()

      # Prepare destination folder.
      if os.path.exists(WRAPREC_PATH):
        shutil.rmtree(WRAPREC_PATH)
      os.makedirs(WRAPREC_PATH)

      # Download and extract the WrapRec package.
      print '[debug] retrieving %s' % WRAPREC_URL
      (temp_file_path, headers) = urllib.urlretrieve(WRAPREC_URL)
      tar_file = tarfile.open(temp_file_path, 'r:gz')
      tar_file.extractall(WRAPREC_PATH)

      # Save depoyed version tag.
      with open(WRAPREC_VERSION_TAG_PATH, 'w') as f:
        f.write('%s\n' % WRAPREC_VERSION)
    except Exception as e:
      # Remove.
      if os.path.exists(WRAPREC_PATH):
        shutil.rmtree(WRAPREC_PATH)

      # Re-raise exception.
      raise e

  @classmethod
  def _install_mono_unix(cls):
    try:
      output = subprocess.check_output([UNIX_INSTALL_MONO])
      print '[debug]', output
    except subprocess.CalledProcessError as e:
      raise IOError('cannot install mono (exit code %d)' % e.returncode)
