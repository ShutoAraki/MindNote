import pymongo
from bson.objectid import ObjectId

class NoteNotFoundException(Exception):
  pass

class Database:
  def __init__(self):
    self.client = pymongo.MongoClient("mongodb+srv://mindnote:mindnote@cluster0-dwh9v.gcp.mongodb.net/test?retryWrites=true&w=majority")
    self.collection = self.client['mindnote']['notes']

  def create_note(self, title, content, vector):
    note = {
      'title': title,
      'content': content,
      'vector': vector,
    }
    inserted_note = self.collection.insert_one(note)
    return {'id': str(inserted_note.inserted_id)}

  def get_note(self, note_id):
    note = self.collection.find_one({'_id': ObjectId(note_id)}, {'_id': 1, 'title': 1, 'content': 1})
    if note is None:
      raise NoteNotFoundException()
    return {'id': str(note['_id']), 'title': note['title'], 'content': note['content']}

  def get_note_vectors(self, note_id):
    pass

  def get_notes(self):
    pass

  def update_note(self, note_id, title, content, vector):
    pass

  def delete_note(self, note_id):
    pass
