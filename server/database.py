import pymongo
from bson.objectid import ObjectId
from datetime import datetime

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
      'last_edit': datetime.now()
    }
    inserted_note = self.collection.insert_one(note)
    return {'id': str(inserted_note.inserted_id)}

  def get_note(self, note_id):
    note = self.collection.find_one({'_id': ObjectId(note_id)}, {'_id': 1, 'title': 1, 'content': 1})
    if note is None:
      raise NoteNotFoundException()
    return {'id': str(note['_id']), 'title': note['title'], 'content': note['content']}

  def get_notes_vectors(self):
    notes = self.collection.find({}, {'_id': 1, 'title': 1 , 'vector': 1, 'content': 1})
    if notes is None:
      raise NoteNotFoundException()
    return [{'id': str(note['_id']), 'title': note['title'], 'vector': note['vector'], 'content': note['content'] if len(note['content']) < 30 else note['content'][:30 - 3] + '...'} for note in notes]

  def get_notes(self):
    notes = self.collection.find({}, {'_id': 1, 'title': 1})
    if notes is None:
      raise NoteNotFoundException()
    return [
      {'id': str(note['_id']), 'title': note['title']}
      for note in notes.sort([('last_edit', pymongo.DESCENDING)])
    ]

  def update_note(self, note_id, title, content, vector):
    note = { '$set' :{
      'title': title,
      'content': content,
      'vector': vector,
      'last_edit': datetime.now()
    }}
    result = self.collection.update_one({'_id': ObjectId(note_id)}, note)
    if result.modified_count == 0:
      raise NoteNotFoundException()

  def delete_note(self, note_id):
    result = self.collection.delete_one({'_id': ObjectId(note_id)})
    if result.deleted_count == 0:
      raise NoteNotFoundException()
