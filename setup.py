from setuptools import setup

setup(
    name='WikiRockWord2Vec',
    version='0.1.0',
    author='aliostad',
    author_email='aliostad [at] gmail [dot] com',
    url='https://github.com/aliostad/WikiRockWord2Vec',
    description='word2vec on Wiki Rock documents',
    zip_safe=False,
    py_modules=['artist_clustering', 'stopword_filtering', 'dictionary_tokenization', 'tokenization',
                'wiki_rock_train', 'wiki_rock_w2v_api', 'artist_clustering', 'wsgi'],
    platforms='any',
    data_files=[('data', ['data/all_artists.txt', 'data/rock_music.w2v', 'data/rock_music.w2v',
                            'data/rock_music.w2v.sun0.npy', 'data/rock_music.w2v.syn1.npy',
                            'data/stop-words-english1.txt', 'data/wiki_rock_multoword_dic.txt'])],
    install_requires=[
        'requests>=2.2.0',
        'gensim',
        'Flask-RESTful>=0.2.12'
    ]
)
