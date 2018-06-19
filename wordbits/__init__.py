"""
Author: Jiashuo Zhang
Date  : 2018.6.12
Name  : wordbits
Func  : provide a user interface for word2vec functions
"""

import os

from flask import Flask, render_template, jsonify, request
from gensim.models import Word2Vec

global model
model = Word2Vec.load('wordbits/word2vec/wiki.zh.text.model')


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

    @app.route('/', methods=['GET'])
    def home():
        return render_template('home.html')

    # a smiple page that says hello
    @app.route('/hello')  # creates a connection between the URL /hello and a function
    @app.route('/hello/<name>')
    def hello(name=None):
        return render_template('hello.html', name=name)

    # register the blueprint word_similarity
    from . import word_similarity
    app.register_blueprint(word_similarity.bp)

    # Create some test data for our catalog in the form of a list of dictionaries.
    books = [
        {'id': 0,
         'title': 'A Fire Upon the Deep',
         'author': 'Vernor Vinge',
         'first_sentence': 'The coldsleep itself was dreamless.',
         'year_published': '1992'},
        {'id': 1,
         'title': 'The Ones Who Walk Away From Omelas',
         'author': 'Ursula K. Le Guin',
         'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
         'published': '1973'},
        {'id': 2,
         'title': 'Dhalgren',
         'author': 'Samuel R. Delany',
         'first_sentence': 'to wound the autumnal city.',
         'published': '1975'}
    ]

    # A route to return all of the available entries in our catalog.
    @app.route('/api/v1/resources/books/all', methods=['GET'])
    def api_all():
        return jsonify(books)

    @app.route('/api/v1/resources/books', methods=['GET'])
    def api_id():
        # Check if an ID was provided as part of the URL.
        # If ID is provided, assign it to a variable.
        # If no ID is provided, display an error in the browser.
        if 'id' in request.args:
            id = int(request.args['id'])
        else:
            return "Error: No id field provided. Please specify an id."

        # Create an empty list for our results
        results = []

        # Loop through the data and match results that fit the requested ID.
        # IDs are unique, but other fields might return many results
        for book in books:
            if book['id'] == id:
                results.append(book)

        # Use the jsonify function from Flask to convert our list of
        # Python dictionaries to the JSON format.
        return jsonify(results)

    return app
