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

    def predict(self, word1, word2=None, n=20):
        predictions = []

        if word2 is not None and len(word2) is not 0:
            predictions = [i[0] for i in autocomplete.predict(first_word=word1, second_word=word2, top_n=n)]
            return  predictions

        for letter in string.ascii_lowercase:
            for p in autocomplete.predict(first_word=word1, second_word=letter, top_n=n):
                predictions.append(p)

        predictions = list(set(predictions))

        predictions = [i[0] for i in sorted(predictions, key=lambda t: t[1], reverse=True)[:n]]
        return predictions


p1 = Predictor("/home/rawand/PycharmProjects/dingocv-api/models/0_all.pkl")
print(p1.predict("Developed"))
