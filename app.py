from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory user storage (dictionary format)
users = {}

# Home route
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the User Management API"}), 200

# GET all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200

# GET a single user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404

# CREATE a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "Invalid data"}), 400
    
    user_id = len(users) + 1
    users[user_id] = {
        "id": user_id,
        "name": data["name"],
        "email": data["email"]
    }
    return jsonify(users[user_id]), 201

# UPDATE a user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    
    users[user_id]["name"] = data.get("name", users[user_id]["name"])
    users[user_id]["email"] = data.get("email", users[user_id]["email"])
    
    return jsonify(users[user_id]), 200

# DELETE a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    del users[user_id]
    return jsonify({"message": "User deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
