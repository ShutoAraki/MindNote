from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__,
    static_url_path='', 
    static_folder='public')
CORS(app, resources={r'/api/*': {'origins': '*'}})

from database import Database, NoteNotFoundException
db = Database()

from vector import VectorGenerator
vector_model = VectorGenerator()

from mapper import Mapper
mapper = Mapper()

from graph_color import generate_colors

@app.route("/api/note", methods=['POST'])
def create_note():
    return jsonify(db.create_note(request.json['title'], request.json['content'], vector_model.generate_vector(request.json['content']), vector_model.generate_sentiment(request.json['content'])))

@app.route("/api/note/<note_id>", methods=['POST'])
def update_note(note_id):
    try:
        jsonify(db.update_note(note_id, request.json['title'], request.json['content'], vector_model.generate_vector(request.json['content']), vector_model.generate_sentiment(request.json['content'])))
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
        if (len(note['vector']) == 4096):
            vectors.append(note['vector'])
        else:
            vectors.append([0.0] * 4096)
        del note['vector']
    coordinates = mapper.compute_map(vectors)
    assert len(notes) == len(coordinates)
    for i in range(len(notes)):
        notes[i]['x'], notes[i]['y'] = coordinates[i]
    
    # Sentiment analysis
    sentiments = list(map(lambda note: note['sentiment'], notes))
    sentiment_colors = generate_colors(sentiments)
    for i in range(len(notes)):
        notes[i]['content'] = notes[i]['content'] if len(notes[i]['content']) < 30 else notes[i]['content'][:30 - 3] + '...'
        notes[i]['color'] = sentiment_colors[i]

    return jsonify(notes)

@app.errorhandler(404)
def page_not_found(e):
    return app.send_static_file('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
