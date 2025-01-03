
# SmartShelf - Food Expiration Tracker

SmartShelf is a simple, intuitive web application designed to help you keep track of your food inventory. The app notifies users about items that are expiring soon and lets users receive email reminders about these items.

---

## Backend Setup

### Navigate to the backend directory:
```bash
cd backend
```

### Install Python dependencies:
```bash
pip install -r requirements.txt
```

### Create a `.env` file in the backend directory with the following content:
```env
SENDGRID_API_KEY=your_sendgrid_api_key
```

### Run the backend server:
```bash
python app.py
```

---

## Frontend Setup

### Navigate to the frontend directory:
```bash
cd frontend
```

### Install Node.js dependencies:
```bash
npm install
```

### Start the frontend server:
```bash
set NODE_OPTIONS=--openssl-legacy-provider && npm start
```

---

## Usage

1. Open your browser and navigate to `http://localhost:3000` to access the app.
2. Add food items with their expiration dates using the form.
3. Monitor the table for food status updates (`Expired`, `Expiring Soon`, or `Fresh`).
4. Use the "Send Email" button to receive email notifications about expiring items.

---

## API Endpoints

### Backend API

- **POST** `/add_food`: Add a new food item.
- **GET** `/food_items`: Retrieve all food items.
- **DELETE** `/delete_food/<id>`: Delete a food item by its ID.
- **POST** `/send_email`: Send an email with expiring/expired food items.

---

## Troubleshooting

### Common Issues

1. **Email not sent**:
   - Ensure your `.env` file contains a valid `SENDGRID_API_KEY`.
   - Check your SendGrid dashboard for email activity.

2. **Frontend not starting**:
   - Use the command: `set NODE_OPTIONS=--openssl-legacy-provider && npm start`.

3. **Backend errors**:
   - Ensure the correct Python dependencies are installed.
   - Restart the Flask server if changes are made to the code.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Contributors

- **Your Name**

Feel free to fork the project, contribute, or report issues. Enjoy using SmartShelf!
