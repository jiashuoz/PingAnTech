"""
Author: Jiashuo Zhang
Date  : 2018.6.12
Name  : wordbits
Func  : provide a user interface for word2vec functions
"""

import os

from flask import Flask, render_template, jsonify, request
from gensim.models import Word2Vec
from flask_restful import Resource, Api
import path_config

global model
model = Word2Vec.load(path_config.wiki_model)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    api = Api(app)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'wordbits.sqlite')
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/', methods=['GET'])
    def home():
        return render_template('home.html')

    # a smiple page that says hello
    @app.route('/hello')  # creates a connection between the URL /hello and a function
    @app.route('/hello/<name>')
    def about(name=None):
        return render_template('about.html', name=name)

    # register the blueprint word_similarity
    from . import word_similarity
    app.register_blueprint(word_similarity.bp)

    class GetSimilarity(Resource):
        def put(self, getsimilarity):
            word1 = request.form['word1']
            word2 = request.form['word2']
            return {"word1": word1,
                    "word2": word2,
                    "score": str(model.wv.similarity(word1, word2))}

    api.add_resource(GetSimilarity, '/<string:getsimilarity>')

    return app
