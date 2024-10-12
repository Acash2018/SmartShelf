from flask import Flask, jsonify

app = Flask(__name__)

# Define a route for the homepage
@app.route('/')
def home():
    return "Welcome to the Simple Flask App!"

# Define a route that returns a JSON response
@app.route('/data')
def get_data():
    return jsonify({"message": "This is a simple JSON response", "status": "success"})

if __name__ == '__main__':
    app.run(debug=True)
