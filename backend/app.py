from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
print("SendGrid API Key:", SENDGRID_API_KEY)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

# In-memory storage for food items
food_items = []
id_counter = 1  # Counter for unique IDs

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
        <li><strong>POST</strong> <code>/send_email</code>: Send an email with expiring/expired food items</li>
    </ul>
    """

# Route to add a food item
@app.route('/add_food', methods=['POST'])
def add_food():
    global id_counter
    data = request.get_json()
    name = data.get('name')
    expiration_date = data.get('expiration_date')

    if not name or not expiration_date:
        return jsonify({"error": "Name and expiration date are required"}), 400

    food_item = {
        "id": id_counter,
        "name": name,
        "expiration_date": expiration_date
    }
    food_items.append(food_item)
    id_counter += 1

    return jsonify({"message": "Food item added successfully", "food_item": food_item}), 201

# Route to get all food items
@app.route('/food_items', methods=['GET'])
def get_food_items():
    return jsonify({"food_items": food_items}), 200

# Route to delete a food item by ID
@app.route('/delete_food/<int:item_id>', methods=['DELETE'])
def delete_food(item_id):
    global food_items
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
    today = datetime.now().date()
    expiring_items = [
        item for item in food_items
        if datetime.strptime(item["expiration_date"], '%Y-%m-%d').date() <= today + timedelta(days=3)
    ]
    return jsonify({"expiring_items": expiring_items}), 200

# Route to send an email with expiring items
@app.route('/send_email', methods=['POST'])
def send_email():
    data = request.get_json()
    recipient_email = data.get('email')

    if not recipient_email:
        return jsonify({"error": "Email is required"}), 400

    today = datetime.now().date()
    expiring_items = [
        item for item in food_items
        if datetime.strptime(item["expiration_date"], '%Y-%m-%d').date() <= today + timedelta(days=3)
    ]

    if not expiring_items:
        return jsonify({"message": "No expiring items to send."}), 200

    item_list = "\n".join([f"{item['name']} (Expires on {item['expiration_date']})" for item in expiring_items])
    email_body = (
        "Here are your expiring or expired items:\n\n"
        f"{item_list}\n\n"
        "Note: All dates are reported in the YYYY-MM-DD format."
    )

    message = Mail(
        from_email='smartshelftracker@gmail.com',
        to_emails=recipient_email,
        subject="Your Expiring Items",
        plain_text_content=email_body
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print("Email sent successfully:", response.status_code)
        return jsonify({"message": "Email sent successfully!"}), 200
    except Exception as e:
        print("Error sending email:", e)
        return jsonify({"error": "Failed to send email"}), 500

if __name__ == '__main__':
    app.run(debug=True)
