from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

# In-memory storage for food items
food_items = []

@app.route('/')
def home():
    return """
    <h1>Welcome to the SmartShelf API!</h1>
    <p>Available endpoints:</p>
    <ul>
        <li><strong>POST</strong> <code>/add_food</code>: Add a new food item</li>
        <li><strong>GET</strong> <code>/food_items</code>: Get all food items</li>
        <li><strong>DELETE</strong> <code>/delete_food/&lt;id&gt;</code>: Delete a food item by ID</li>
        <li><strong>PUT</strong> <code>/update_food/&lt;id&gt;</code>: Update a food item by ID</li>
        <li><strong>GET</strong> <code>/notify_expiring</code>: Get expiring food items</li>
    </ul>
    """


# Route to add a food item
@app.route('/add_food', methods=['POST'])
def add_food():
    global id_counter
    data = request.get_json()

    # Validate incoming data
    name = data.get('name')
    expiration_date = data.get('expiration_date')

    if not name or not expiration_date:
        return jsonify({"error": "Name and expiration date are required"}), 400

    # Create and append a new food item with an incrementing ID
    food_item = {
        "id": id_counter,  # Use the counter for unique IDs
        "name": name,
        "expiration_date": expiration_date
    }
    food_items.append(food_item)
    id_counter += 1  # Increment the counter for the next item

    return jsonify({"message": "Food item added successfully", "food_item": food_item}), 201


# Route to get all food items
@app.route('/food_items', methods=['GET'])
def get_food_items():
    return jsonify({"food_items": food_items}), 200


# Route to delete a food item by ID
@app.route('/delete_food/<int:item_id>', methods=['DELETE'])
def delete_food(item_id):
    global food_items
    # Filter out the item with the given ID
    print(f"Current food items: {food_items}")  # Debugging
    print(f"Attempting to delete item with ID: {item_id}")
    food_items = [item for item in food_items if item["id"] != item_id]
    return jsonify({"message": f"Food item with ID {item_id} deleted"}), 200


# Route to update a food item by ID
@app.route('/update_food/<int:item_id>', methods=['PUT'])
def update_food(item_id):
    data = request.get_json()
    for item in food_items:
        if item["id"] == item_id:
            item["name"] = data.get("name", item["name"])
            item["expiration_date"] = data.get("expiration_date", item["expiration_date"])
            return jsonify({"message": f"Food item with ID {item_id} updated", "food_item": item}), 200
    return jsonify({"error": "Food item not found"}), 404


# Route to notify about expiring items
@app.route('/notify_expiring', methods=['GET'])
def notify_expiring():
    from datetime import datetime, timedelta

    today = datetime.now().date()
    expiring_items = [
        item for item in food_items
        if datetime.strptime(item["expiration_date"], '%m-%d-%Y').date() <= today + timedelta(days=3)
    ]
    return jsonify({"expiring_items": expiring_items}), 200


if __name__ == '__main__':
    app.run(debug=True)
