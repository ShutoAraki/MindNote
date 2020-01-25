from gensim.models.doc2vec import Doc2Vec
import nltk
from nltk.tokenize import word_tokenize
import urllib.request
import os
from zipfile import ZipFile
import torch

nltk.download('punkt')

model_file = 'models.py'
if not os.path.isfile(model_file):
  urllib.request.urlretrieve('https://raw.githubusercontent.com/facebookresearch/InferSent/master/models.py', model_file)
from models import InferSent

fast_text_folder = 'fastText'
if not os.path.isdir(fast_text_folder):
  os.mkdir(fast_text_folder)
  urllib.request.urlretrieve('https://dl.fbaipublicfiles.com/fasttext/vectors-english/crawl-300d-2M.vec.zip', 'crawl-300d-2M.vec.zip')
  zf = ZipFile('crawl-300d-2M.vec.zip')
  zf.extractall(path = fast_text_folder)
  zf.close()
  os.remove('crawl-300d-2M.vec.zip')

if not os.path.isdir('encoder'):
  os.mkdir('encoder')
  urllib.request.urlretrieve('https://dl.fbaipublicfiles.com/infersent/infersent2.pkl', 'encoder/infersent.pkl')
  
class VectorGenerator:
  def __init__(self, model_path='encoder/infersent.pkl'):
    params_model = {'bsize': 64, 'word_emb_dim': 300, 'enc_lstm_dim': 2048,
                'pool_type': 'max', 'dpout_model': 0.0, 'version': 2}
    self.model = InferSent(params_model)
    self.model.load_state_dict(torch.load(model_path))
    self.model.set_w2v_path('fastText/crawl-300d-2M.vec')
    self.model.build_vocab_k_words(K=100000)

  def generate_vector(self, text):
    return list(map(lambda value: value.item(), self.model.encode([text], tokenize=True)[0]))
