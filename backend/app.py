from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
import os
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///csv_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True  # Enable to see SQL queries in the console

# Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "*"}})

db = SQLAlchemy(app)

print(f"Database file location: {os.path.abspath('csv_data.db')}")

# Model to store CSV data
class CSVData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(100))
    data = db.Column(db.Text)  # Store the CSV data as JSON string

# Create the database tables
with app.app_context():
    db.create_all()

# Endpoint to upload CSV data
@app.route('/api/upload_csv', methods=['POST'])
def upload_csv():
    data = request.get_json()
    print("Received data:", data)  # Debugging log to show received data
    file_name = data.get('fileName')
    csv_data = data.get('data')

    if not file_name or not csv_data:
        print("Invalid data received.")
        return jsonify({"error": "Invalid data"}), 400

    # Append a timestamp to the file name to ensure uniqueness
    unique_file_name = f"{file_name}_{int(time.time())}"

    try:
        # Convert CSV data to JSON string for storing
        new_csv = CSVData(file_name=unique_file_name, data=json.dumps(csv_data))
        db.session.add(new_csv)
        db.session.commit()
        print(f"Successfully saved file: {unique_file_name} with data: {csv_data}")

        # Debugging: Print all records in the database after saving
        all_files = CSVData.query.all()
        print(f"Total files in database: {len(all_files)}")
        for file in all_files:
            print(f"File: {file.file_name}, Data: {file.data}")

    except Exception as e:
        print(f"Failed to save CSV data: {str(e)}")
        return jsonify({"error": f"Failed to save CSV data: {str(e)}"}), 500

    return jsonify({"message": "CSV data saved successfully"}), 200

# Endpoint to get all uploaded CSV files
@app.route('/api/get_csv_files', methods=['GET'])
def get_csv_files():
    try:
        csv_files = CSVData.query.all()
        if not csv_files:
            print("No files found in the database.")
        else:
            print(f"Retrieved {len(csv_files)} file(s) from the database.")
            for file in csv_files:
                print(f"File: {file.file_name}, Data: {file.data}")
        result = [
            {"fileName": file.file_name, "data": json.loads(file.data)}
            for file in csv_files
        ]
        return jsonify(result), 200
    except Exception as e:
        print(f"Failed to retrieve files: {str(e)}")
        return jsonify({"error": f"Failed to retrieve files: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
