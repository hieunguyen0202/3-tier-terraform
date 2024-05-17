from flask import Flask, request, jsonify
import mysql.connector
import bcrypt  

from config import DATABASE_CONFIG

app = Flask(__name__)

# MySQL configurations
db = mysql.connector.connect(**DATABASE_CONFIG)
cursor = db.cursor()

# Create a table to store user data if it doesn't exist
create_table_query = """
    CREATE TABLE IF NOT EXISTS user (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        email VARCHAR(255),
        Address TEXT,
        phonenumber VARCHAR(255),
        password VARCHAR(255)
    )
"""
cursor.execute(create_table_query)
db.commit()




@app.route('/health')
def home():
    return "Home healthy"


@app.route('/api/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Extract data from request
        data = request.json

        # Hash the password before storing it
        password = data['password'].encode('utf-8')
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        # Insert user data into the database
        insert_query = "INSERT INTO user (name, email, Address, phonenumber, password) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (data['name'], data['email'], data['address'], data['phonenumber'], hashed_password))
        db.commit()

        # Fetch the latest entry
        cursor.execute("SELECT * FROM user ORDER BY id DESC LIMIT 1")
        data = cursor.fetchall()

        return jsonify(data)

@app.route('/api/get-data', methods=['POST'])
def get_data():
    if request.method == 'POST':
        # Retrieve data based on user input ID
        input_id = request.json['input_id']
        # Query database for data based on input_id
        cursor.execute("SELECT * FROM user WHERE id = %s", (input_id,))
        data = cursor.fetchall()
        return jsonify(data)

@app.route('/api/delete/<int:id>', methods=['GET', 'POST'])
def delete_data(id):
    if request.method == 'POST':
        # Perform deletion based on the provided ID
        delete_query = "DELETE FROM user WHERE id = %s"
        cursor.execute(delete_query, (id,))
        db.commit()
        return "Data deleted successfully"


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=5000)