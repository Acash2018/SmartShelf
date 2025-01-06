SmartShelf

SmartShelf is a web application to track food expiration and notify users about expiring items via email.

Features

Add food items with expiration dates.

View food status (Expired, Expiring Soon, or Fresh).

Send email notifications about expiring items.

Backend Setup

Navigate to the backend directory:

cd backend

Install Python dependencies:

pip install -r requirements.txt

Create a .env file in the backend directory with the following content:

SENDGRID_API_KEY=your_sendgrid_api_key

Run the backend server:

python app.py

Frontend Setup

Navigate to the frontend directory:

cd frontend

Install Node.js dependencies:

npm install

Start the frontend server:

set NODE_OPTIONS=--openssl-legacy-provider && npm start

Usage

Open your browser and navigate to http://localhost:3000 to access the app.

Add food items with their expiration dates using the form.

Monitor the table for food status updates (Expired, Expiring Soon, or Fresh).

Use the "Send Email" button to receive email notifications about expiring items.

Email Notifications

The email includes a list of items that are either expired or expiring soon.

Dates are reported in the YYYY-MM-DD format.

API Endpoints

Backend API

POST /add_food: Add a new food item.

GET /food_items: Retrieve all food items.

DELETE /delete_food/<id>: Delete a food item by its ID.

POST /send_email: Send an email with expiring/expired food items.

Troubleshooting

Common Issues

Email not sent:

Ensure your .env file contains a valid SENDGRID_API_KEY.

Check your SendGrid dashboard for email activity.

Frontend not starting:

Use the command: set NODE_OPTIONS=--openssl-legacy-provider && npm start.

Backend errors:

Ensure the correct Python dependencies are installed.

Restart the Flask server if changes are made to the code.

License

This project is licensed under the MIT License.

Contributors

Your Name

Feel free to fork the project, contribute, or report issues. Enjoy using SmartShelf!

