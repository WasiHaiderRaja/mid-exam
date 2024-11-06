from flask import Flask, request, jsonify
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Database connection function
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="shopease",
        user="postgres",
        password="yourpassword"
    )
    return conn

# User Registration Endpoint
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    # Hash the password for security
    hashed_password = generate_password_hash(password, method='sha256')
    
    # Insert the user into the database
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)",
                    (username, hashed_password))
        conn.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

    return jsonify({"message": "User registered successfully!"}), 201

# User Login Endpoint
@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data['username']
    password = data['password']

    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT password FROM users WHERE username = %s", (username,))
    user = cur.fetchone()

    cur.close()
    conn.close()

    if user and check_password_hash(user[0], password):
        return jsonify({"message": "Login successful!"}), 200
    else:
        return jsonify({"message": "Invalid username or password!"}), 401

# Home route
@app.route('/')
def home():
    return "Welcome to ShopEase User Service!"

if __name__ == '__main__':
    app.run(debug=True)
