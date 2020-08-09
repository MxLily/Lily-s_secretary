import os

class FileFinder(object):
  '''
  '''
  def __init__(self):
    pass

  def gatherFiles(self, directory: str, files: list):
    '''
    '''
    if not directory.endswith('/'):
      directory += '/'
    listdir = os.listdir(directory)
    for it in listdir:
      fullpath = directory + it
      if os.path.isfile(fullpath) and fullpath.endswith('.py'):
        files.append(fullpath)
      elif os.path.isdir(fullpath):
        self.gatherFiles(fullpath, files)

  def find(self, directory: str, extension: str):
    '''
    '''
    if not os.path.isdir(directory):
      print('Directory: \'' + directory + '\' doesn\'t exist or isn\'t a directory. Please verify given name.')
    else:
      files = []
      self.gatherFiles(directory, files)
      return files
    return []
