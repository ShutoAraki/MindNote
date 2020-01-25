from gensim.models.doc2vec import Doc2Vec
import nltk
from nltk.tokenize import word_tokenize

nltk.download('punkt')

replaced_values = [
  '-',
  '...',
  '*'
]

class VectorGenerator:
  def __init__(self, model_path='d2v.model'):
    self.model = Doc2Vec.load(model_path)

  def generate_vector(self, text):
    for value in replaced_values:
      text = text.replace(value, '')
    return list(map(lambda value: value.item(), self.model.infer_vector(word_tokenize(text.lower()))))
