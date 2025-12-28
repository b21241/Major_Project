from flask import Flask, request, jsonify

app = Flask(__name__)

# Temporary in-memory storage - data will be lost when server stops
users = []
notes = []


# GET endpoint - View all notes
@app.route("/notes/<int:user_id>", methods=["GET"])
def get_user_notes(user_id):
    user_notes = [n for n in notes if n["user_id"] == user_id]

    return jsonify({
        "user_id": user_id,
        "notes": user_notes,
        "count": len(user_notes)
    }), 200


@app.route("/users", methods=["POST"])
def create_user():
    data = request.json

    if not data or "name" not in data:
        return jsonify({"error": "name is required"}), 400

    user = {
        "id": len(users) + 1,
        "name": data["name"]
    }

    users.append(user)

    return jsonify({
        "message": "User created successfully",
        "user": user
    }), 201


@app.route("/notes", methods=["POST"])
def create_note():
    data = request.json

    if not data or "user_id" not in data:
        return jsonify({"error": "user_id is required"}), 400

    # check user exists
    user = next((u for u in users if u["id"] == data["user_id"]), None)
    if not user:
        return jsonify({"error": "User not found"}), 404

    note = {
        "id": len(notes) + 1,
        "user_id": data["user_id"],
        "title": data.get("title"),
        "content": data.get("content")
    }

    notes.append(note)

    return jsonify({
        "message": "Note created successfully",
        "note": note
    }), 201


if __name__ == "__main__":
    app.run(debug=True)
