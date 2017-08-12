import os
import uuid

from flask import render_template

from app import app, db

from config import base_dir


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
