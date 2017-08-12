import string

import autocomplete


class Predictor(object):
    def __init__(self, model_file):
        self._model_file = model_file
        print(self.model_file)
        autocomplete.models.load_models(load_path=self.model_file)

    @property
    def model_file(self):
        return self._model_file

    @model_file.setter
    def model_file(self, value):
        self._model_file = value

    def predict(self, word1, word2, n=10):
        predictions = []
        if len(word2) is not 0:
            return autocomplete.predict(first_word=word1, second_word=word2, top_n=n)

        for letter in string.ascii_lowercase:
            for p in autocomplete.predict(first_word=word1, second_word=letter, top_n=n):
                predictions.append(p)

        predictions = sorted(predictions, key=lambda t: t[1], reverse=True)[:n]
        return predictions


p1 = Predictor("/home/rawand/PycharmProjects/dingocv-api/models/22_information_technology.pkl")
print(p1.predict("android", "k"))
