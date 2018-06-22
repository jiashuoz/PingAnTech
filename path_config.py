import os

root = os.path.dirname(__file__) + '/'

wordbits_path = root + 'wordbits/'

wordbits_model = wordbits_path + 'models/'

wiki_model = wordbits_model + 'word2vec/wiki.zh.text.model'
big_model = wordbits_model + '120g_model/news_12g_baidubaike_20g_novel_90g_embedding_64.model'