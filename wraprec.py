import os
import subprocess

from config import BASE_PATH

BIN_DEPLOY = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          'wraprec_deploy.sh')

BIN_WRAPREC = os.path.join(BASE_PATH, 'wraprec', 'WrapRec.exe')

class PyWrapRec(object):

  def __init__(self):
    raise Exception('Cannot instantiate. Call PyWrapRec.run(config_file_path) '
                    'as static method.')

  @classmethod
  def run(cls, config_file_path):
    cls.check_dependencies()
    # TODO(alessio): call BIN_WRAPREC

  @classmethod
  def check_dependencies(cls):
    if not cls._is_wraprec_deployed():
      cls._deploy_wraprec()

  @classmethod
  def _is_wraprec_deployed(cls):
    return os.path.exists(BIN_WRAPREC)

  @classmethod
  def _deploy_wraprec(cls):
    print '[notice] deploying WrapRec'
    exit_code = subprocess.call([BIN_DEPLOY])
    if exit_code != 0:
      raise IOError('cannot deploy WrapRec (exit code %d)' % exit_code)
    assert cls._is_wraprec_deployed()
