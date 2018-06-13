"""
Author: Jiashuo Zhang
Date  : 2018.6.12
Name  : wordbits
Func  : provide a user interface for word2vec functions
"""

import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
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

    # a smiple page that says hello
    @app.route('/hello')  # creates a connection between the URL /hello and a function
    def hello():
        return 'Hello, World!'

    # register the blueprint word_similarity
    from . import word_similarity
    app.register_blueprint(word_similarity.bp)

    return app
