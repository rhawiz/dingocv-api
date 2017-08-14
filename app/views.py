import os

import re
from flask import request, jsonify

from app import app, db
from app.core.predict import Predictor

from config import base_dir


@app.route('/', methods=['GET'])
def home():
    return "Dingo CV API"


@app.route('/predict', methods=['GET'])
def predict():
    if request.method == 'GET':
        w1 = request.args.get('w1')
        w2 = request.args.get('w2', '')
        n = request.args.get('n', 10)
        cat = request.args.get('cat', 0)

        path = model_selector(cat)

        predictor = Predictor(model_file=path)
        res = predictor.predict(w1, w2, n=int(n))
        return jsonify(res)


models_path = os.path.join(base_dir, 'models')


def model_selector(cat):
    files = os.listdir(models_path)
    model_file = ''
    for f in files:
        srch = re.search("[0-9]+", f)

        num = srch.group() if srch is not None else 0

        if str(cat) == str(num):
            model_file = f
            print(model_file)
            break

    return os.path.join(models_path, model_file)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True, reloader_type='auto')
