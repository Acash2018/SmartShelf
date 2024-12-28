from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food_items.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model for Food Item
class FoodItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    expiration_date = db.Column(db.String(10), nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "expiration_date": self.expiration_date}

# Initialize the database
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return """
        <h1>Welcome to the SmartShelf API!</h1>
        <p>Available endpoints:</p>
        <ul>
            <li>/add_food (POST)</li>
            <li>/food_items (GET)</li>
            <li>/delete_food/&lt;id&gt; (DELETE)</li>
            <li>/update_food/&lt;id&gt; (PUT)</li>
            <li>/notify_expiring (GET)</li>
        </ul>
    """

# Add new food
@app.route('/add_food', methods=['POST'])
def add_food():
    data = request.get_json()
    name = data.get('name')
    expiration_date = data.get('expiration_date')

    if not name or not expiration_date:
        return jsonify({"error": "Missing name or expiration date"}), 400

    # Check for duplicate food items
    existing_item = FoodItem.query.filter_by(name=name, expiration_date=expiration_date).first()
    if existing_item:
        return jsonify({"error": "Food item with the same name and expiration date already exists."}), 400

    # Add new food item
    new_food = FoodItem(name=name, expiration_date=expiration_date)
    db.session.add(new_food)
    db.session.commit()

    return jsonify({"message": "Food item added successfully", "food_item": new_food.to_dict()}), 201

# Get all food items
@app.route('/food_items', methods=['GET'])
def get_food_items():
    items = FoodItem.query.all()
    return jsonify({"food_items": [item.to_dict() for item in items]}), 200

# Update a food item by ID
@app.route('/update_food/<int:item_id>', methods=['PUT'])
def update_food(item_id):
    data = request.get_json()
    item = FoodItem.query.get(item_id)

    if item:
        item.name = data.get('name', item.name)
        expiration_date = data.get('expiration_date')

        if expiration_date:
            try:
                expiration_date_obj = datetime.strptime(expiration_date, '%m-%d-%Y').date()
                item.expiration_date = expiration_date_obj.strftime('%m-%d-%Y')
            except ValueError:
                return jsonify({"error": "Invalid expiration date format. Use MM-DD-YYYY."}), 400
        
        db.session.commit()
        return jsonify({"message": "Food item updated", "food_item": item.to_dict()}), 200
    return jsonify({"error": "Item not found"}), 404

# Delete a food item by ID
@app.route('/delete_food/<int:item_id>', methods=['DELETE'])
def delete_food(item_id):
    item = FoodItem.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Food item deleted", "removed_item": item.to_dict()}), 200
    return jsonify({"error": "Item not found"}), 404

# Notify for items expiring in 3 days
@app.route('/notify_expiring', methods=['GET'])
def notify_expiring():
    today = datetime.now().date()
    expiring_items = FoodItem.query.filter(
        FoodItem.expiration_date <= (today + timedelta(days=3)).strftime('%m-%d-%Y')
    ).all()

    return jsonify({"expiring_items": [item.to_dict() for item in expiring_items]}), 200

if __name__ == '__main__':
    app.run(debug=True)
