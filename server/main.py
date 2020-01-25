from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify
app = Flask(__name__)

from database import Database, NoteNotFoundException
db = Database()

from vector import VectorGenerator
vector_model = VectorGenerator()

from mapper import Mapper
mapper = Mapper()

@app.route("/api/note", methods=['POST'])
def create_note():
    return jsonify(db.create_note(request.json['title'], request.json['content'], vector_model.generate_vector(request.json['content'])))

@app.route("/api/note/<note_id>", methods=['POST'])
def update_note(note_id):
    try:
        jsonify(db.update_note(note_id, request.json['title'], request.json['content'], vector_model.generate_vector(request.json['content'])))
        return jsonify({})
    except:
        return jsonify({}), 404

@app.route("/api/note/<note_id>", methods=['DELETE'])
def delete_note(note_id):
    try:
        db.delete_note(note_id)
        return jsonify({})
    except NoteNotFoundException:
        return jsonify({}), 404

@app.route("/api/note/<note_id>", methods=['GET'])
def get_note(note_id):
    try:
        return jsonify(db.get_note(note_id))
    except NoteNotFoundException:
        return jsonify({}), 404

@app.route("/api/notes", methods=['GET'])
def get_notes():
    try:
        return jsonify(db.get_notes())
    except NoteNotFoundException:
        return jsonify({}), 404

@app.route("/api/map", methods=['GET'])
def get_map():
    notes = db.get_notes_vectors()
    if len(notes) == 0:
        return jsonify([])
    vectors = []
    for note in notes:
        vectors.append(note['vector'])
        del note['vector']
    coordinates = mapper.compute_map(vectors)
    assert len(notes) == len(coordinates)
    for i in range(len(notes)):
        notes[i]['x'], notes[i]['y'] = coordinates[i]
    return jsonify(notes)

if __name__ == "__main__":
    app.run()
