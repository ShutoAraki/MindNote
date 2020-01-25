from dotenv import load_dotenv
load_dotenv()

from flask import Flask
app = Flask(__name__)

from database import Database
db = Database()

@app.route("/api/notes")
def get_notes():
    return db.get_notes()

if __name__ == "__main__":
    app.run()
