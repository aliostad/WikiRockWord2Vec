import codecs
import tokenization

class WordNode:

  def __init__(self):
    self.__leaves = {}  # words
    self.__nodes = {}  # child nodes

  '''
  word => a Multiword
  '''
  def add_word(self, word, level=0):

    currentToken = word.get_segment(level)

    if level == word.get_length() - 1:
      if currentToken not in self.__leaves:
        self.__leaves[currentToken] = word

    else:
      if currentToken not in self.__nodes:
        self.__nodes[currentToken] = WordNode()
      self.__nodes[currentToken].add_word(word, level+1)

  '''
    :tokens => array of string (tokens/words)
    :returns => None if finds node but no leaf (Multiword), true if finds a leaf and false if definitely doesn't find
  '''
  def find_entries_in_phrase(self, tokens):

    results = []
    i = 0
    j = 0
    while j < len(tokens):
      currentPhrase = [tokens[j]]  # create a list and add jth token
      breadth = 1

      if j == len(tokens) - 1:
        results.append(tokens[j])     # end of text
        break

      while True:

        if j + breadth >= len(tokens):
          break   # end of text

        currentPhrase.append(tokens[j+breadth])
        result = self.__find_phrase(currentPhrase)
        if isinstance(result, Multiword):
          results.append(' '.join(currentPhrase))
          j += breadth
          break

        breadth += 1
        if result is not None:   # only happens if False
          results.append(tokens[j])
          break

      j += 1

    return results

  def __find_phrase(self, tokens, level=0):

    currentToken = tokens[level]
    if level == len(tokens) - 1:
      if currentToken in self.__leaves:
        return self.__leaves[currentToken]
      else:
        return None if currentToken in self.__nodes else None
      # return self.__leaves[currentToken] if currentToken in self.__leaves else False
    else:
      return self.__nodes[currentToken].__find_phrase(tokens, level+1) if currentToken in self.__nodes else False

#______________________________________________________________________________________________

class Multiword:

  def __init__(self, segments, allword_dic = None):


    self.__segments = []
    for s in segments:
      self.__segments.append(s)
      # NAUGH
      if allword_dic is not None:
        if s not in allword_dic:
          allword_dic[s] = None


  def get_segment(self, i):
    if i >= len(self.__segments):
      print(1)
    return self.__segments[i]

  def get_fullword(self):
    return ' '.join(self.__segments)

  def get_length(self):
    return len(self.__segments)

#___________________________________________________________________________________________

class DictionaryBasedMultiwordFinder:

  __default_dictionary_path = "multiwords_in_corpus.txt"

  def __init__(self, **kwargs):

    self.__wordtree = WordNode()
    __allword_dic = {}
    dictionary_path = self.__default_dictionary_path
    if("dictionary_path" in kwargs):
      dictionary_path = kwargs["dictionary_path"]

    tknzr = self.__tokeniseLine
    if("tokeniser" in kwargs):
      tknzr = kwargs["tokeniser"]

    isverbose = False
    if("verbose" in kwargs):
      isverbose = kwargs["verbose"]

    f = codecs.open(dictionary_path, encoding="UTF-8")
    n = 0
    while True:
      line = f.readline().rstrip()
      n += 1

      if isverbose and n % 100000 == 0:
        print(n)

      if (line is None or line == ""):
        break
      words = tknzr(line)
      self.__wordtree.add_word(Multiword(words, __allword_dic))

    f.close()

  # ONLY USED FOR MULTI-WORD PARSING
  @classmethod
  def __tokeniseLine(cls, text):
    return text.split(" ")

  def tokenise(self, text, **kwargs):

    tknzr = tokenization.segment_simple
    if("tokeniser" in kwargs):
      tknzr = kwargs["tokeniser"]

    tokens = tknzr(text)
    return self.__wordtree.find_entries_in_phrase(tokens)


#______________________________________________________________________________________________


