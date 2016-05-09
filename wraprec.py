import os
import platform
import shutil
import subprocess
import sys
import tarfile
import urllib

from config import BASE_PATH

UNIX_INSTALL_MONO = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          'install_mono.sh')

WRAPREC_PATH = os.path.join(BASE_PATH, 'wraprec')

WRAPREC_BIN = os.path.join(WRAPREC_PATH, 'WrapRec.exe')

WRAPREC_URL = ('https://github.com/babakx/WrapRec/releases/download/{0}/'
               'wraprec.{0}.tar.gz'.format('2.0.3'))

PLATFORM = platform.system()

class PyWrapRec(object):

  def __init__(self):
    raise Exception('Cannot instantiate. Call PyWrapRec.run(config_file_path) '
                    'as static method.')

  @classmethod
  def run(cls, config_file_path):
    cls.check_dependencies()
    try:
      # WrapRec needs to run from the data directory.
      working_directory = os.path.dirname(config_file_path)
      assert os.path.isdir(working_directory)

      # Build arguments list.
      args = cls._get_command() + [config_file_path]

      # Create a new process.
      process = subprocess.Popen(args, cwd=working_directory, bufsize=4096)
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
    # TODO(alessio): parse output file with libpandas.
    pass

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
    return os.path.exists(WRAPREC_BIN)

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
