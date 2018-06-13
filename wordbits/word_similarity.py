import functools
from gensim.models import Word2Vec

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('word_similarity', __name__, url_prefix='/word_similarity')


@bp.route('/compare', methods=('GET', 'POST'))
def compare():
    score = int(-1)
    if request.method == 'POST':
        firstword = request.form['firstword']
        secondword = request.form['secondword']
        error = None

        if not firstword:
            error = 'first word is required.'
        elif not secondword:
            error = 'second word is required.'

        model = Word2Vec.load('./word2vec/wiki.zh.text.model')

        try:
            score = model.wv.similarity(firstword, secondword)
        except KeyError:
            error = 'one of the words does not exist.'

        flash(error)
    return render_template('word_similarity/compare.html', score=score)
