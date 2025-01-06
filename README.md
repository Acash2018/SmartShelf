SmartShelf
  SmartShelf is a web application to track food expiration and notify users about expiring items via email.

Features
  Add food items with expiration dates.
  View food status (Expired, Expiring Soon, or Fresh).
  Send email notifications about expiring items.

Backend Setup
  Navigate to the backend directory: cd backend
  Install Python dependencies: pip install -r requirements.txt
  Create a .env file in the backend directory with the following content:
    SENDGRID_API_KEY=your_sendgrid_api_key
  Run the backend server:
    python app.py

Frontend Setup
  Navigate to the frontend directory: cd frontend
  Install Node.js dependencies: npm install
Start the frontend server: set NODE_OPTIONS=--openssl-legacy-provider && npm start

Usage
1. Open your browser and navigate to http://localhost:3000 to access the app.
2. Add food items with their expiration dates using the form.
3. Monitor the table for food status updates (Expired, Expiring Soon, or Fresh).
4. Use the "Send Email" button to receive email notifications about expiring items.

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
    Email not sent: Ensure your .env file contains a valid SENDGRID_API_KEY. Check your SendGrid dashboard for email activity.\

Setting Up Email Notifications
  To enable email notifications, you'll need a SendGrid account. Follow these steps:
    1. Sign up at [SendGrid](https://sendgrid.com/).
    2. Generate an API key by going to **Settings > API Keys** in your SendGrid dashboard.
    3. Create a `.env` file in the `backend` directory and add the following line:
   ```
   SENDGRID_API_KEY=your_sendgrid_api_key
   ```
   4. Save the file. Do not commit this file to the repository.

Setting Up the Sender Email
  To send emails using this application, you'll need to configure a verified sender email:
    1. Log in to your SendGrid account.
    2. Go to **Settings > Sender Authentication**.
    3. Add and verify your email address (e.g., `your_email@example.com`).
    4. Add the email address to your `.env` file:
   ```
   SENDER_EMAIL=your_verified_email@example.com
   ```


Frontend not starting: Use the command: set NODE_OPTIONS=--openssl-legacy-provider && npm start.

Backend errors:
  Ensure the correct Python dependencies are installed.
  Restart the Flask server if changes are made to the code.

Contributors: Aakash Tripathi

Enjoy using SmartShelf!

