# WikiRockWord2Vec
[![Build Status](https://travis-ci.org/aliostad/WikiRockWord2Vec.svg?branch=master)](https://travis-ci.org/aliostad/WikiRockWord2Vec)

A small word2vec project to illustrate its power when trained even on the smallest datasets.

Project is Python 2.7 and uses gensim to build word2vec model on a small dataset of Rock music entries in Wikipedia.

The dataset can be downloaded from [here](https://drive.google.com/file/d/0By4PF7Jis9FzTTFpS1VVVzB4NFk/view?usp=sharing).

See the blog post with more information [here](http://byterot.blogspot.co.uk/2015/07/daft-punk-tool-muse-word2vec-model-trained-36K-rock-music-corpus-wiki-NLP-gensim.html).

## Example API
```
http://rockword2vecapi-dev.elasticbeanstalk.com/api/v1/rock/similar?pos=<comma separate list>&neg=<comma separated list>
```
For example:


[http://rockword2vecapi-dev.elasticbeanstalk.com/api/v1/rock/similar?pos=Radiohead](http://rockword2vecapi-dev.elasticbeanstalk.com/api/v1/rock/similar?pos=Radiohead)
