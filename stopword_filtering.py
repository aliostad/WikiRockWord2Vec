import codecs

class StopwordFilter:

  def __init__(self, dictionary_fileName):

    f = codecs.open(dictionary_fileName, mode='r', encoding='utf-8')

    self.__stopwords = {}
    while True:
      line = f.readline()

      if line == None or line == '':
        break

      self.__stopwords[line.strip()] = None

  '''
  words: a list of phrases and words
  '''
  def filter(self, words):

    result = []
    for word in words:
      if word not in self.__stopwords:
        result.append(word)

    return result