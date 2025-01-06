from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import json
app=Flask(__name__)
CORS(app)

food_items = []

def load_food_items():
    global food_items
    try:
        with open('food_items.json','r') as file:
            food_items=json.load(file)
        except FileNotFoundError:
            food_items=[]

def save_food_items():
    with open('food_items.json','w') as file:
        json.dump(food_items,file)
def add_food():
    data=request.get_json()
    food_name=data.get('name')
    expiration_data=data.get('expiration_date')

    if not food_name or not expiration_date:
        return jsonify({"error":"Missing name or expiration date"}),400

    food_items.append({
        "name":food_name
        "expiration_date": expiration_date
    })
    save_food_items()
    return jsonify({"message": "Food item added successfully","food_items":food_items}),

def get_food_items():
    return jsonify({"food_items": food_items}), 200

def delete_food(item_id):
    if item_id<0 or item_id >= len(food_items):
        return jsonify({"error":"Item not found"}), 404
    
    removed_item = food_items.pop(item_id)
    save_food_items()
    return jsonify({"message":"Food item deleted","removed_item": removed_item}), 200

def notify_expiring():
    today=datetime.now().date()
    expiring_items=[
        items for item in food_items
        if datetime.strptime(item["expiration_date"],'%Y-%m-%d').date()<=today+timedelta(days=3)

    ]
    return jsonify({"expiring_items": expiring_items}), 200



if __name__ == '__main__':
    load_food_items()
    app.run(debug=True)
    