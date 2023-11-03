import os
from loguru import logger

class Directory:
    def __init__(self, directory):
        self.cwd = None
        self.directory = directory

    def __enter__(self):
        self.cwd = os.getcwd()
        os.chdir(self.directory)

    def __exit__(self, *_):
        os.chdir(self.cwd)

catch_exit = logger.catch(onerror=lambda _: exit())