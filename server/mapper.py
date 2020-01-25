import numpy as np
from MulticoreTSNE import MulticoreTSNE as TSNE

class Mapper:
  def __init__(self):
    self.tsne = TSNE(n_jobs=-1, n_iter=10000, perplexity=40)

  def compute_map(self, vectors):
    vectors = np.array(vectors)

    return self.tsne.fit_transform(vectors).tolist()
