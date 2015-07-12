# encoding: utf-8
from __future__ import unicode_literals
import codecs
import glob
import time
import stopword_filtering
import tokenization
import gensim
import dictionary_tokenization

class EnglishSentences(object):
  def __init__(self, globPattern, tknsr, debug=False):
    self.globPattern = globPattern
    self.debug = debug
    self.tknsr = tknsr

  def __iter__(self):
    i = 0
    for f in glob.glob(self.globPattern):
      i+=1
      txt = get_text(f)
      for sentence in tokenization.segment_to_sentences(txt):
        yield self.tknsr(sentence)
      if self.debug and i % 100 == 0:
        print(i)


class Corpus:

  def __init__(self, globPattern, dic, tokenisr, debug=False):
    self._glob_pattern = globPattern
    self._dic = dic
    self._debug = debug
    self._tokeniser = tokenisr

  def __iter__(self):
    i = 0
    for f in glob.glob(self._glob_pattern):
      fs = codecs.open(f, encoding="utf-8", mode="r")
      txt = fs.read()
      fs.close()
      words = self._tokeniser(txt)
      i += 1
      if self._debug and i % 100 == 0:
        print(i)
      yield self._dic.doc2bow(words)

def get_text(fileName):
  f = codecs.open(fileName, mode='r', encoding='utf-8')
  txt = f.read()
  f.close()
  return txt

def train_and_save(multiword_dic_path, stopword_path, corpus_files_glob_pattern, mode_file_name = 'rock_music.w2v'):
  tknsr = dictionary_tokenization.DictionaryBasedMultiwordFinder(dictionary_path=multiword_dic_path)
  filtr = stopword_filtering.StopwordFilter(stopword_path)
  tokenizze = lambda text: filtr.filter(tknsr.tokenise(text))
  wvc = gensim.models.Word2Vec(EnglishSentences(corpus_files_glob_pattern, tokenizze, True), min_count=2)
  wvc.save(mode_file_name)


'''
# Uncomment to train =>

train_and_save('data/wiki_rock_multiword_dic.txt', 'data/stop-words-english1.txt',
               '<THE_LOCATION>/wiki_rock_corpus/*.txt')

'''