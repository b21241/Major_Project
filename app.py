from flask import Flask, request, jsonify
from datetime import date as date_class, datetime
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)


# ------- MySQL Connection Configuration -------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "yogesh@123",
    "database": "notes_db"
}


def get_db_connection():
    """
    Create and return a MySQL database connection.
    Creates a new connection each time (better for handling timeouts and concurrent requests).
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def get_cursor(connection):
    """Get a dictionary cursor from the connection"""
    return connection.cursor(dictionary=True)


# Test database connection endpoint
@app.route("/test-db", methods=["GET"])
def test_db_connection():
    """Test if database connection is working"""
    db = None
    try:
        db = get_db_connection()
        if db and db.is_connected():
            cursor = get_cursor(db)
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            cursor.close()
            db.close()
            return jsonify({
                "status": "success",
                "message": "Database connection successful",
                "mysql_version": version.get("VERSION()") if version else None
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": "Failed to connect to database"
            }), 500
    except Error as e:
        return jsonify({
            "status": "error",
            "message": f"Database connection failed: {str(e)}"
        }), 500
    finally:
        if db and db.is_connected():
            db.close()


@app.route("/notes/<int:user_id>", methods=["GET"])
def get_user_notes(user_id):
    """Get notes for a specific user, optionally filtered by date"""
    db = None
    cursor = None
    try:
        db = get_db_connection()
        if not db:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = get_cursor(db)
        req_date = request.args.get("date")

        if req_date:
            query = "SELECT * FROM notes WHERE user_id = %s AND date = %s"
            cursor.execute(query, (user_id, req_date))
        else:
            query = "SELECT * FROM notes WHERE user_id = %s"
            cursor.execute(query, (user_id,))

        user_notes = cursor.fetchall()
        
        # Convert date objects to YYYY-MM-DD format
        for note in user_notes:
            if note.get('date') and isinstance(note['date'], (date_class, datetime)):
                note['date'] = note['date'].strftime("%Y-%m-%d")

        return jsonify({
            "user_id": user_id,
            "count": len(user_notes),
            "notes": user_notes
        }), 200
    except Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    finally:
        if cursor:
            cursor.close()
        if db and db.is_connected():
            db.close()


@app.route("/users", methods=["POST"])
def create_user():
    """Create a new user"""
    db = None
    cursor = None
    try:
        data = request.json

        if not data or "name" not in data:
            return jsonify({"error": "name is required"}), 400

        db = get_db_connection()
        if not db:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = get_cursor(db)
        query = "INSERT INTO users (name) VALUES (%s)"
        values = (data["name"],)

        cursor.execute(query, values)
        db.commit()

        user_id = cursor.lastrowid

        return jsonify({
            "message": "User created successfully",
            "user_id": user_id
        }), 201
    except Error as e:
        if db:
            db.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    finally:
        if cursor:
            cursor.close()
        if db and db.is_connected():
            db.close()


@app.route("/notes", methods=["POST"])
def create_note():
    """Create a new note"""
    db = None
    cursor = None
    try:
        data = request.json

        if not data or "user_id" not in data:
            return jsonify({"error": "user_id is required"}), 400

        db = get_db_connection()
        if not db:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = get_cursor(db)

        # Check if user exists
        cursor.execute("SELECT * FROM users WHERE id = %s", (data["user_id"],))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404

        # Insert note
        query = """
            INSERT INTO notes (user_id, title, content, date)
            VALUES (%s, %s, %s, %s)
        """
        
        values = (
            data["user_id"],
            data.get("title"),
            data.get("content"),
            data.get("date", str(date_class.today()))
        )

        cursor.execute(query, values)
        db.commit()

        note_id = cursor.lastrowid

        return jsonify({
            "message": "Note created successfully",
            "note_id": note_id
        }), 201
    except Error as e:
        if db:
            db.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    finally:
        if cursor:
            cursor.close()
        if db and db.is_connected():
            db.close()


if __name__ == "__main__":
    app.run(debug=True)
