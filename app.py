from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import uuid
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# In-memory storage for food items (or you can use a database)
food_items = []

# Load food items from a JSON file at startup (optional)
def load_food_items():
    global food_items
    try:
        with open('food_items.json', 'r') as file:
            food_items = json.load(file)
            # Convert expiration dates back to 'MM-DD-YYYY' format
            for item in food_items:
                item['expiration_date'] = datetime.strptime(item['expiration_date'], '%m-%d-%Y').strftime('%m-%d-%Y')
    except FileNotFoundError:
        food_items = []

# Save food items to a JSON file (optional)
def save_food_items():
    with open('food_items.json', 'w') as file:
        json.dump(food_items, file)

@app.route('/')
def home():
    return "Welcome to the SmartShelf API! Available endpoints: /add_food, /food_items, /delete_food/<id>, /update_food/<id>, /notify_expiring"

@app.route('/add_food', methods=['POST'])
def add_food():
    data = request.get_json()
    food_name = data.get('name')
    expiration_date = data.get('expiration_date')

    if not food_name or not expiration_date:
        return jsonify({"error": "Missing name or expiration date"}), 400
    
    # Validate expiration date format (MM-DD-YYYY)
    try:
        expiration_date = datetime.strptime(expiration_date, '%m-%d-%Y').date()
    except ValueError:
        return jsonify({"error": "Invalid expiration date format. Use MM-DD-YYYY."}), 400

    # Check for duplicate food items
    if any(item['name'] == food_name and item['expiration_date'] == expiration_date.strftime('%m-%d-%Y') for item in food_items):
        return jsonify({"error": "Food item with the same name and expiration date already exists."}), 400

    food_items.append({
        "id": str(uuid.uuid4()),  # Assign unique ID
        "name": food_name,
        "expiration_date": expiration_date.strftime('%m-%d-%Y')  # Store as string for consistency
    })

    save_food_items()  # Save to file
    return jsonify({"message": "Food item added successfully", "food_items": food_items}), 201

@app.route('/food_items', methods=['GET'])
def get_food_items():
    return jsonify({"food_items": food_items}), 200

# Update the delete_food route to delete by unique ID
@app.route('/delete_food/<string:item_id>', methods=['DELETE'])
def delete_food(item_id):
    item = next((item for item in food_items if item['id'] == item_id), None)
    if item:
        food_items.remove(item)
        save_food_items()
        return jsonify({"message": "Food item deleted", "removed_item": item}), 200
    return jsonify({"error": "Item not found"}), 404

@app.route('/update_food/<string:item_id>', methods=['PUT'])
def update_food(item_id):
    data = request.get_json()
    item = next((item for item in food_items if item['id'] == item_id), None)
    
    if item:
        # Update the item if it's found
        item['name'] = data.get('name', item['name'])  # Update name if provided
        expiration_date = data.get('expiration_date')
        
        # Update expiration date if provided and valid
        if expiration_date:
            try:
                expiration_date = datetime.strptime(expiration_date, '%m-%d-%Y').date()
                item['expiration_date'] = expiration_date.strftime('%m-%d-%Y')
            except ValueError:
                return jsonify({"error": "Invalid expiration date format. Use MM-DD-YYYY."}), 400
        
        save_food_items()  # Save changes to file
        return jsonify({"message": "Food item updated", "food_item": item}), 200
    return jsonify({"error": "Item not found"}), 404

@app.route('/notify_expiring', methods=['GET'])
def notify_expiring():
    today = datetime.now().date()
    expiring_items = [
        item for item in food_items
    if datetime.strptime(item["expiration_date"], '%m-%d-%Y').date() <= today + timedelta(days=3)
    ]
    return jsonify({"expiring_items": expiring_items}), 200


# Define a route for the homepage
@app.route('/')
def home():
    return """
        <h1>Welcome to the SmartShelf API!</h1>
        <p>Available endpoints:</p>
        <ul>
            <li>/add_food (POST)</li>
            <li>/food_items (GET)</li>
            <li>/delete_food/<id> (DELETE)</li>
            <li>/update_food/<id> (PUT)</li>
            <li>/notify_expiring (GET)</li>
        </ul>
    """

# Define a route that returns a JSON response
@app.route('/data')
def get_data():
    return jsonify({"message": "This is a simple JSON response", "status": "success"})

if __name__ == '__main__':
    load_food_items()  
    app.run(debug=True)
