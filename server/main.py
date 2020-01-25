from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify
app = Flask(__name__)

from database import Database, NoteNotFoundException
db = Database()

from vector import VectorGenerator
vector_model = VectorGenerator()

@app.route("/api/note", methods=['POST'])
def create_note():
    print(request.json)
    return jsonify(db.create_note(request.json['title'], request.json['content'], vector_model.generate_vector(request.json['content'])))

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

if __name__ == "__main__":
    app.run()
