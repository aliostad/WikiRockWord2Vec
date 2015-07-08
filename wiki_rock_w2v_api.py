from __future__ import unicode_literals
from flask import Flask, jsonify, request
import logging
from logging import FileHandler
import time
import gensim

t = time.time()
if __name__ == '__main__':
  print("Time is now {}".format(t))

app = Flask(__name__)
application = app

try:
  file_handler = FileHandler("wordsim_api.log", "a")
  file_handler.setLevel(logging.WARNING)
  app.logger.addHandler(file_handler)
  word_sim = gensim.models.Word2Vec.load('data/rock_music.w2v')
  if __name__ == '__main__':
    print("Took {}".format(time.time() - t))
except:
  if __name__ == '__main__':
    print("could not start file logging")


def order_sims(similars, minFreq = 10):
  res = []
  similars = sorted(similars, key=lambda x: x[1], reverse=True)
  for c in similars:
    if word_sim.vocab[c[0]].count > minFreq:
      res.append(c)
  return res

@app.route('/api/v1/rock/similar', methods=['GET'])
def similar():

  poss = request.args.get('pos')
  negs = request.args.get('neg')
  topns = request.args.get('topn')
  min_freqs = request.args.get('min_freq')

  pos = [] if poss==None else map(lambda x: x, poss.split(','))
  neg = [] if negs==None else map(lambda x: x, negs.split(','))
  topn = 100 if topns==None else int(topns)
  min_freq = 10 if min_freqs==None else int(min_freqs)

  for p in pos:
    if p not in word_sim.vocab:
      return jsonify({"result": "Not in vocab: " + p}), 400

  for p in neg:
    if p not in word_sim.vocab:
      return jsonify({"result": "Not in vocab: " + p}), 400

  if word_sim is None:
    raise ValueError("word_sim is none")

  sims = word_sim.most_similar(positive=pos, negative=neg, topn=topn)
  return jsonify({"result": order_sims(sims, min_freq)})

if __name__ == '__main__':
  app.run(debug = True, use_reloader=False)

