# Import necessary libraries
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
from flask_bcrypt import Bcrypt
import os  # Import the os module
from flask_cors import CORS  # Import CORS

# Load environment variables from the .env file
from dotenv import load_dotenv
load_dotenv()

# Create a Flask web application
app = Flask(__name__)

CORS(app)  # Enable CORS for all routes

# Initialize Flask-Bcrypt for password hashing
bcrypt = Bcrypt(app)

# MongoDB configuration
# Use the environment variable to get the MongoDB URI
mongodb_uri = os.getenv("MONGODB_URI")
client = MongoClient(mongodb_uri)  # Use the URI from the environment variable
db = client["users"]
users_collection = db["users"]
user_data_collection = db["users"]


# Define a route for the homepage
@app.route('/')
def index():
    return "Welcome to User API"

# User Registration and Login endpoints

# Endpoint for store book
@app.route('/storebook', methods=['POST'])
def register():
    # Extract data from the request
    bookTitle = request.form.get('bookTitle')
    bookAuthor = request.form.get('bookAuthor')
    bookEdition = request.form.get('bookEdition')
    bookLanguage = request.form.get('bookLanguage')
    bookCategory = request.form.get('bookCategory')
    bookRate = request.form.get('bookRate')
    bookSellerContact = request.form.get('bookSellerContact')
    bookImage = request.files.get('bookImage')

    # Check if any of the required fields are missing
    if not (bookTitle and bookAuthor and bookEdition and bookLanguage and bookCategory and bookRate and bookSellerContact and bookImage):
        return jsonify({'message': 'All fields are required'}), 400

    # You can perform actions with the book details and the uploaded image here.
    # For example, you can save the image to a directory and store the file path in your database.

    # Assuming you want to save the book details in the "users" collection
    book_data = {
        "bookTitle": bookTitle,
        "bookAuthor": bookAuthor,
        "bookEdition": bookEdition,
        "bookLanguage": bookLanguage,
        "bookCategory": bookCategory,
        "bookRate": bookRate,
        "bookSellerContact": bookSellerContact
        # You can add more fields as needed
    }
    
    # Insert the book data into the MongoDB collection
    users_collection.insert_one(book_data)

    # For this example, we'll just return a success message.
    return jsonify({'message': 'Book registered successfully'}), 201


# Endpoint for user login
@app.route('/login', methods=['POST'])
def login():
    # Extract email and password from the request
    email = request.json['email']
    password = request.json['password']

    # Find the user with the provided email
    user = users_collection.find_one({'email': email})

    # Check if the user exists and the password is correct
    if user and bcrypt.check_password_hash(user['password'], password):
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401


# Run the Flask app if this script is executed
if __name__ == '__main__':
    app.run(debug=True)
