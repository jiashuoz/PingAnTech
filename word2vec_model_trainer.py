import logging
import os.path
import sys
import multiprocessing

from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence


class ModelTrainer:

    # A word2vec model trainer based on gensim
    def __init__(self):
        self.model_adx = ""
        self.data_adx = ""
        self.vect_adx = ""

    def set_model_adx(self, model_adx):
        self.model_adx = model_adx

    def set_data_adx(self, data_adx):
        self.data_adx = data_adx

    def set_vector_adx(self, vect_adx):
        self.vect_adx = vect_adx

    def train_model(self, size=128, window=5, min_count=5, workers=1):
        program = os.path.basename(sys.argv[0])
        logger = logging.getLogger(program)

        logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
        logging.root.setLevel(level=logging.INFO)
        logger.info("running %s" % ' '.join(sys.argv))

        # check and process input arguments
        # if len(sys.argv) < 4:
        #     print(globals()['__doc__'] % locals())
        #     sys.exit(1)
        sentences = LineSentence(self.data_adx)

        if os.path.isfile(self.model_adx):
            model = Word2Vec.load(self.model_adx)
            model.build_vocab(sentences, update=True)
            model.train(sentences, total_examples=model.corpus_count, epochs=model.iter)
        else:
            model = Word2Vec(sentences, size=size, window=window, min_count=min_count, workers=workers)

        # trim unneeded model memory = use(much) less RAM
        # model.init_sims(replace=True)
        model.save(self.model_adx)

        # model.save_word2vec_format(outp2, binary=False)
        model.wv.save(self.vect_adx)


if __name__ == "__main__":
    model_trainer = ModelTrainer()
    model_trainer.set_data_adx()
