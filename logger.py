import logging
from logging import CRITICAL, ERROR, WARNING, INFO, DEBUG
# from logging import handlers
from os import remove

def createLogger(name, LOG_LEVEL):
  logger=logging.getLogger(name)
  logger.setLevel(LOG_LEVEL)
  try:
    remove('info.log')
  except:
    pass
  fh = logging.FileHandler('info.log')
  fh.setLevel(LOG_LEVEL)

  # create formatter
  formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

  # add formatter to ch
  fh.setFormatter(formatter)

  # add ch to logger
  logger.addHandler(fh)
  return logger


class MyLogSet(dict):
  def __init__(self, *args, LOG_LEVEL=DEBUG):
    for arg in args:
      try:
        self[arg]=createLogger(arg,LOG_LEVEL)
      except Exception as e:
        print(f"ERROR creating logfile: {e}")



class MyLogger():
  def __init__(self,name,LOG_LEVEL):
    self.log_level=LOG_LEVEL
    # create logger
    self.logger = logging.getLogger(name)
    self.logger.setLevel(LOG_LEVEL)

    try:
      remove('info.log')
    except:
      pass
    # create console handler and set level to debug
    fh = logging.FileHandler('info.log')
    fh.setLevel(LOG_LEVEL)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

    # add formatter to ch
    fh.setFormatter(formatter)

    # add ch to logger
    self.logger.addHandler(fh)


  def write(self, buf):
      for line in buf.rstrip().splitlines():
         self.logger.log(self.log_level, line.rstrip())

  def flush(self):
    pass

  def debug(self,str):
    self.logger.debug(str)

  def info(self,str):
    self.logger.info(str)

  def warning(self,str):
    self.logger.warning(str)

  def error(self,str):
    self.logger.error(str)
