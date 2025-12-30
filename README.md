# Notes API

A Flask REST API for managing user notes with MySQL database integration.

## Features

- **User Management**: Create new users
- **Notes Management**: Create and retrieve notes for users
- **Date Filtering**: Filter notes by specific date
- **Database Connection Testing**: Test endpoint to verify MySQL connectivity

## API Endpoints

### Test Database Connection
```
GET /test-db
```
Tests the MySQL database connection and returns the MySQL version.

### Create User
```
POST /users
Content-Type: application/json

{
  "name": "Yogesh"
}
```
Creates a new user and returns the user ID.

### Create Note
```
POST /notes
Content-Type: application/json

{
  "user_id": 1,
  "title": "My Note",
  "content": "Note content here",
  "date": "2024-01-15"  // Optional, defaults to today
}
```
Creates a new note for a user. Requires `user_id`, `title` and `content` are optional.

### Get User Notes
```
GET /notes/<user_id>?date=2024-01-15
```
Retrieves all notes for a specific user. Optionally filter by date using the `date` query parameter.

## Database Configuration

The app connects to MySQL with the following configuration:
- **Host**: localhost
- **Database**: notes_db
- **User**: root

Update the `DB_CONFIG` dictionary in `app.py` to match your MySQL setup.

## Requirements

- Python 3.13.3
- Flask 3.1.2
- mysql-connector-python

## Running the Application

```bash
python app.py
```

The server will start on `http://localhost:5000` with debug mode enabled.

