# coding=utf-8

punc_sign = u'#'

_delimiters = [' ', '\t', '.', '\r', '\n', ':', '.', '-', ',', ';', '['
                    , ']', '{', '}', '(', ')', '/', '\\', '\'', '@', '"', '!',
                    u'£', u'€', '#', '?', '!', '%', '&', '*', '_', '+', '=', '>', '<',
                    '`', '~', '|', '،', ' ', u'«', u'»', u'،', u'؛']

_delimitersMap = {}.fromkeys(_delimiters, 1)

_whitespaces = [u' ', u'\t', u'\r', u'\n']
_punctuations = [u'.', u',', u'!', u'?', u':', u';',  u'-', u'·', u'(', u')', u'[', u']', u'=', u'{', u'}',
                 u'،', u'؛', u'٬',  u'‑', u'–', u'—', u'.', u'·', u'٫', u'؟', u'/', u'\\', u'<', u'>' ]
_stopsigns = [u'.', u'!', u'?', u':', u';',  u'-', u'·', u'؛', u'–', u'—', u'·', u'؟']

_quotes = {u'\'': u'\'', u'"': u'"', u'‘': u'’', u'’': u'‘', u'‚': u'‛', u'‛': u'‚', u'“': u'”',
           u'”': u'“', u'„': u'“', u'«': u'»', u'»': u'«'}

_replacements = {
    0x26: None, # &
    0x2a: None, # *
    0x2b: None, # +
    0x23: None # (#)
  }

class SegmentationResult:

  def __init__(self, words, phrases):
    self.__words = words
    self.__phrases = phrases

  def get_phrases(self):
    return self.__phrases

  def get_words(self):
    return self.__words

  def get_words_nophrasesplitter(self):
    res = []
    for w in self.__words:
      if w != punc_sign:
        res.append(w)
    return res

def split_text(text, delimiters=_delimitersMap):

  word_buffer = []
  char_buffer = []
  for ch in text:
    if(ch in delimiters):
      if(len(char_buffer)>0):
        word_buffer.append(reduce(lambda x, y: x+y, char_buffer))
        char_buffer = []
    else:
      char_buffer.append(ch)

  if(len(char_buffer)>0):
    word_buffer.append(reduce(lambda x, y: x+y, char_buffer))

  return word_buffer


def segment(text, replacements=_replacements,
            whitespaces=_whitespaces,
            punctuations=_punctuations,
            quotes=_quotes):

  text_rep = text.translate(replacements)

  terminator_to_look_for = None
  words = []
  phrases = []
  current_phrase_start = -1
  current_word_start = -1
  position = 0

  for ch in text_rep:

    # if we are looking for a phrase
    if terminator_to_look_for is not None:

      # if it is the terminator we are looking for
      if ch == terminator_to_look_for:
        terminator_to_look_for = None
        # if we already have an open phrase
        if current_phrase_start >= 0:
          phrases.append(text_rep[current_phrase_start:position])
          current_phrase_start = -1
      # if not the terminator looking for
      else:
        # if not have an open phrase open one
        if current_phrase_start == -1:
          current_phrase_start = position
    else:
      if ch in quotes:
        terminator_to_look_for = quotes[ch]

    # word
    if ch in quotes or ch in punctuations or ch in whitespaces:
      if current_word_start >= 0:
        words.append(word_normaliser(text_rep[current_word_start:position]))
        current_word_start = -1
        if ch in punctuations:
          words.append(punc_sign)
    else:
      if current_word_start == -1:
        current_word_start = position

    position += 1

  if current_word_start > 0:
    w = text_rep[current_word_start:position]
    if len(w) > 0:
      words.append(w)

  return SegmentationResult(words, phrases)

def segment_to_paragraphs(text):

  paras = text.split('\n')
  paras_trimmed = map(lambda x: x.strip(), paras)
  result = []
  for para in paras_trimmed:
   if len(para) > 20:
     result.append(para)
  return result


def select_first_n_paragraphs(text, n):

  paras = segment_to_paragraphs(text)
  result = ""
  for i in range(0, n):
    if i < len(paras):
      result += (paras[i] + " ")

  return result

def _segment_to_sentences_deprecated(text):

  stopsigns = { u'. ':None, u'! ':None, u'? ':None, u'؟ ':None, u'· ': None,
                u'.\t':None, u'!\t':None, u'?\t':None, u'؟\t':None, u'·\t': None,
                u'.\n':None, u'!\n':None, u'?\n':None, u'؟\n':None, u'·\n': None,
                u'.\r':None, u'!\r':None, u'?\r':None, u'؟\r':None, u'·\r': None}  # punctuation plus space
  previous_start = 0
  results = []
  for i in range(1, len(text)):
    if text[i-1:i] in stopsigns:
      results.append(text[previous_start:i-1])
      previous_start = i+1

  if previous_start < len(text)-2: # last sentence
    results.append(text[previous_start:len(text)-1])

  return results

def segment_to_sentences(text):

  previous_start = 0
  results = []
  for i in range(0, len(text)):
    if text[i] in _stopsigns:
      results.append(text[previous_start:i])
      previous_start = i+1

  if previous_start < len(text)-1: # last sentence
    results.append(text[previous_start:len(text)-1])

  return results

def segment_simple(text, replacements=_replacements,
            whitespaces=_whitespaces,
            punctuations=_punctuations,
            quotes=_quotes):
  return segment(text, replacements, whitespaces, punctuations, quotes).get_words_nophrasesplitter()

def select_first_n_sentences(text, n):

  snts = segment_to_sentences(text)
  result = ""
  for i in range(0, n):
    if i < len(snts):
      result += (snts[i] + " ")

  return result


