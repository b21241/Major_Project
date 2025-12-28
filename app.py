from flask import Flask, request, jsonify
from datetime import date as date_class

app = Flask(__name__)

users = []
notes = []


@app.route("/notes/<int:user_id>", methods=["GET"])
def get_user_notes(user_id):
    user_notes = [n for n in notes if n["user_id"] == user_id]

    req_date = request.args.get("date")
    if req_date:
        user_notes = [n for n in user_notes if n["date"] == req_date]

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
    print("Received Body:", data)     # DEBUG
    print("Notes before:", notes)     # DEBUG

    if not data or "user_id" not in data:
        return jsonify({"error": "user_id is required"}), 400

    user = next((u for u in users if u["id"] == data["user_id"]), None)
    if not user:
        return jsonify({"error": "User not found"}), 404

    note = {
        "id": len(notes) + 1,
        "user_id": data["user_id"],
        "title": data.get("title"),
        "content": data.get("content"),
        "date": data.get("date", str(date_class.today()))
    }

    notes.append(note)

    print("Notes after:", notes)      # DEBUG
    print("Note dictionary:", note)   # DEBUG - verify date is in note dict

    return jsonify({
        "message": "Note created successfully",
        "note": note
    }), 201


if __name__ == "__main__":
    app.run(debug=True)
