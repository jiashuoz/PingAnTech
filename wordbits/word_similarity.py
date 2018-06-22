from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,
    jsonify)

from wordbits import model

bp = Blueprint('word_similarity', __name__, url_prefix='/word_similarity')


@bp.route('/compare', methods=['GET', 'POST'])
def compare():
    score = int(0)
    firstword = None
    secondword = None
    if request.method == 'POST':
        firstword = request.form['firstword']
        secondword = request.form['secondword']
        error = "Please check the score:"

        if not firstword:
            error = 'first word is required.'
        elif not secondword:
            error = 'second word is required.'

        try:
            score = model.wv.similarity(firstword, secondword)
        except KeyError:
            error = 'one of the words does not exist.'

        flash(error)
    return render_template('word_similarity/compare.html', score=score, word1=firstword, word2=secondword)


@bp.route('/compare/api', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'word1' in request.args and 'word2' in request.args:
        word1 = str(request.args['word1'])
        word2 = str(request.args['word2'])
    else:
        return "Error: No words field provided. Please specify two words to compare."

    # Create an empty list for our results
    results = []
    error = None
    score = None
    try:
        score = model.wv.similarity(word1, word2)
    except KeyError:
        error = 'one of the words does not exist.'

    results.append({'1st word': word1,
                    '2nd word': word2,
                    'similarity': score})

    flash(error)
    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)
