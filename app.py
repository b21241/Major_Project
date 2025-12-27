from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("notes.db")
    conn.row_factory = sqlite3.Row
    return conn


# ---------- DB Setup ----------
def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT,
            content TEXT,
            note_date DATE
        );
    """)
    conn.commit()
    conn.close()

init_db()


# ---------- CREATE NOTE ----------
@app.route("/notes", methods=["POST"])
def create_note():
    conn = None
    try:
        data = request.json
        conn = get_db()
        conn.execute(
            "INSERT INTO notes (user_id, title, content, note_date) VALUES (?, ?, ?, ?)",
            (data["user_id"], data["title"], data["content"], data["note_date"])
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "Note created successfully"}), 201
    except Exception as e:
        if conn:
            conn.close()
        return jsonify({"error": str(e)}), 400


# ---------- FETCH NOTES BY USER + DATE ----------
@app.route("/users/<int:user_id>/notes", methods=["GET"])
def get_notes(user_id):
    date = request.args.get("date")

    if not date:
        return jsonify({"error": "date query param required (YYYY-MM-DD)"}), 400

    conn = None
    try:
        conn = get_db()
        cursor = conn.execute(
            "SELECT * FROM notes WHERE user_id = ? AND note_date = ?",
            (user_id, date)
        )

        notes = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify({
            "user_id": user_id,
            "date": date,
            "notes": notes
        }), 200
    except Exception as e:
        if conn:
            conn.close()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
