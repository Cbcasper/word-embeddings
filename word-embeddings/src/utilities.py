import os

class Directory:
    def __init__(self, directory):
        self.directory = directory

    def __enter__(self):
        os.chdir(self.directory)

    def __exit__(self, *_):
        os.chdir("..")