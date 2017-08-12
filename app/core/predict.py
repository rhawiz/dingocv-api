import os

from config import base_dir


class Predictor(object):
    def __init__(self, cat_id, models_dir=os.path.join(base_dir, 'models')):
        self._cat_id = cat_id
        self._models_dir = models_dir

    @property
    def cat_id(self):
        return self._cat_id

    @cat_id.setter
    def cat_id(self, value):
        self._cat_id = value

    @property
    def models_dir(self):
        return self._models_dir

    @models_dir.setter
    def models_dir(self, value):
        self._models_dir = value

