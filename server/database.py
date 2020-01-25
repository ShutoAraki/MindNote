import pymongo

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

  def get_note(self, id):
    pass

  def get_note_vectors(self, id):
    pass

  def get_notes(self):
    pass

  def update_note(self, id, title, content, vector):
    pass

  def delete_note(self, id):
    pass
