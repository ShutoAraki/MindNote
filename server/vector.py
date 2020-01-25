from gensim.models.doc2vec import Doc2Vec
import nltk
from nltk.tokenize import word_tokenize
import urllib.request
import os
from zipfile import ZipFile
import torch
import sys
import time

nltk.download('punkt')
nltk.download('vader_lexicon')

from nltk.sentiment.vader import SentimentIntensityAnalyzer

def reporthook(count, block_size, total_size):
  global start_time
  if count == 0:
      start_time = time.time()
      return
  duration = time.time() - start_time
  progress_size = int(count * block_size)
  speed = int(progress_size / (1024 * duration))
  percent = int(count * block_size * 100 / total_size)
  sys.stdout.write("\r...%d%%, %d MB, %d KB/s, %d seconds passed" %
                  (percent, progress_size / (1024 * 1024), speed, duration))
  sys.stdout.flush()

model_file = 'models.py'
if not os.path.isfile(model_file):
  urllib.request.urlretrieve('https://raw.githubusercontent.com/facebookresearch/InferSent/master/models.py', model_file, reporthook)
from models import InferSent

fast_text_folder = 'fastText'
if not os.path.isdir(fast_text_folder):
  os.mkdir(fast_text_folder)
  urllib.request.urlretrieve('https://dl.fbaipublicfiles.com/fasttext/vectors-english/crawl-300d-2M.vec.zip', 'crawl-300d-2M.vec.zip', reporthook)
  zf = ZipFile('crawl-300d-2M.vec.zip')
  zf.extractall(path = fast_text_folder)
  zf.close()
  os.remove('crawl-300d-2M.vec.zip')

if not os.path.isdir('encoder'):
  os.mkdir('encoder')
  urllib.request.urlretrieve('https://dl.fbaipublicfiles.com/infersent/infersent2.pkl', 'encoder/infersent.pkl', reporthook)

class VectorGenerator:
  def __init__(self, model_path='encoder/infersent.pkl'):
    params_model = {'bsize': 64, 'word_emb_dim': 300, 'enc_lstm_dim': 2048,
                'pool_type': 'max', 'dpout_model': 0.0, 'version': 2}
    self.model = InferSent(params_model)
    self.model.load_state_dict(torch.load(model_path))
    self.model.set_w2v_path('fastText/crawl-300d-2M.vec')
    self.model.build_vocab_k_words(K=100000)

    self.sentiment_model = SentimentIntensityAnalyzer()

  def generate_vector(self, text):
    return list(map(lambda value: value.item(), self.model.encode([text], tokenize=True)[0]))

  def generate_sentiment(self, text):
    return self.sentiment_model.polarity_scores(text)['compound']
