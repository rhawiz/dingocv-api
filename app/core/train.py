import os
import re

from config import base_dir, logger

SELECT_CAT_PHRASE_QUERY = """
SELECT phrases.id,
       phrases.phrase,
       phrases.total_exp_months,
       phrases.job_exp_months,
       phrases.education,
       jobs.job_title,
       categories.category
  FROM phrases
       LEFT JOIN
       jobs ON phrases.job_id = jobs.id
       LEFT JOIN
       categories ON category_id = categories.id

WHERE category_id = {cat_id}
"""

SELECT_ALL_CATEGORIES_QUERY = """SELECT id, category, category_code, description from categories"""
SELECT_CATEGORY_QUERY = """SELECT id, category, category_code, description from categories WHERE id={cat_id}"""

from autocomplete.models import train_models
import sqlite3


class AutocompleteTrainer(object):
    def __init__(self, categories=None, save_dir='models/', sqlite_path='../../dingocv_phrases.sqlite'):
        """
        :param categories: List of ints containing category ids to train, if set to None or empty list all categories will be trained
        :param save_dir: Directory path to save autocomplete models
        :param sqlite_path: Path to sqlite database file
        """

        self._save_dir = save_dir
        self._cursor = self._connect(sqlite_path)
        if categories is None or len(categories) is 0 or not isinstance(categories, (list, tuple)):
            categories = self._get_categories()
        self._categories = categories
        self._mapping = {}

    @property
    def categories(self):
        return self._categories

    @categories.setter
    def categories(self, value):
        self._categories = value

    @property
    def mapping(self):
        return self._mapping

    @mapping.setter
    def mapping(self, value):
        self._mapping = value

    @property
    def save_dir(self):
        return self._save_dir

    @save_dir.setter
    def save_dir(self, value):
        self._save_dir = value

    @property
    def cursor(self):
        return self._cursor

    @cursor.setter
    def cursor(self, value):
        self._cursor = value

    def _connect(self, sqlite_path):
        conn = sqlite3.connect(sqlite_path)
        conn.text_factory = bytes
        return conn.cursor()

    def train(self):

        for cat_id in self.categories:
            query = SELECT_CAT_PHRASE_QUERY.format(cat_id=cat_id)
            cat_details = self._get_category_details(cat_id)
            cat_code = cat_details.get('category_code')
            cat_name = cat_details.get('category')
            fname = '{}_{}.pk'.format(cat_id, cat_code).replace(" ", "").replace("-", "_")
            dir = os.path.join(base_dir, self.save_dir)

            if not os.path.exists(dir):
                os.makedirs(dir)

            path = os.path.join(dir, fname)
            logger.info("Generating corpus for {}".format(cat_name))
            corpus = self._generate_corpus(query)
            logger.info("Training model for {}".format(cat_name))
            train_models(corpus, model_name=path)
            self._mapping[cat_id] = path
            logger.info("Saved model to {}".format(path))

        return self._mapping

    def _get_category_details(self, cat_id):
        id, category, category_code, description = self.cursor.execute(
            SELECT_CATEGORY_QUERY.format(cat_id=cat_id)).fetchone()

        return {
            'id': id,
            'category': category.decode('utf-8'),
            'category_code': category_code.decode('utf-8'),
            'description': description.decode('utf-8')
        }

    def _get_categories(self):
        categories = []
        for _id, cat, code, desc in self.cursor.execute(SELECT_ALL_CATEGORIES_QUERY):
            categories.append(_id)
        return categories

    def _generate_corpus(self, query):
        corpus = ""

        res = self.cursor.execute(query)
        data = res.fetchall()
        for row in data:
            phrase = row[1]
            pre_processed = self._pre_process(phrase)
            corpus += " {}".format(pre_processed)
        return corpus

    def _pre_process(self, phrase):
        if isinstance(phrase, bytes):
            try:
                phrase = phrase.decode("utf-8")
            except UnicodeDecodeError:
                phrase = phrase.decode("latin-1")
        processed = phrase.lower()
        processed = re.sub(r'[^0-9a-zA-Z]+', ' ', processed)
        processed = re.sub(r'[^\x00-\x7F]+', ' ', processed)
        processed = processed.strip()

        return processed

    def close(self):
        if self.cursor is not None:
            self.cursor.close()

            #
            # ac = AutocompleteTrainer([1, 4])
            # ac.train()
            # print(ac.mapping)
