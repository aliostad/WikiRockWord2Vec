from __future__ import unicode_literals
import gensim
import codecs
from scipy import cluster
import time
import numpy as np

def load_model():
  return gensim.models.Word2Vec.load('data/rock_music.w2v')

def get_all_artists():
  return {}.fromkeys(map(lambda x: x.strip(), codecs.open('data/all_artists.txt'))).keys()

def build_vectors(model):
  vecs = []
  names = []
  for a in get_all_artists():
    if a in model:
      vecs.append(model[a])
      names.append(a)
  return vecs, names


def build_clusters():
  model = load_model()
  data, names = build_vectors(model)
  a, b = cluster.vq.kmeans2(np.array(data), 300)
  clusters = {}

  for i in range(0, len(b)):
    clusNo = b[i]
    artist = names[i]

    if clusNo not in clusters:
      clusters[clusNo] = []
    clusters[clusNo].append(artist)
  return clusters

def report_clusters(clusters):
  for c in clusters:
    print(', '.join(clusters[c]))
    print('\n\n\n')

