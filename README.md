Tech Stack
The SmartShelf project is built using the following technologies:

Frontend
React.js: A JavaScript library for building user interfaces, enabling a responsive and dynamic experience for managing food items.
HTML5 & CSS3: Used to structure and style the components of the application.
Bootstrap: A CSS framework for responsive and mobile-first design.
Backend
Flask: A lightweight Python web framework for creating RESTful APIs and handling backend logic.
Flask-CORS: Handles Cross-Origin Resource Sharing (CORS) to enable communication between the frontend and backend.
SendGrid API: Provides the email-sending functionality for notifying users about expiring or expired items.
Database
In-Memory Storage: Food items are stored temporarily during runtime. (Future scope: Integration with a database for persistent storage.)
Other Tools & Libraries
dotenv: For loading environment variables, including sensitive keys like the SendGrid API key.
SendGrid Helper Libraries: Used for constructing and sending emails with the SendGrid API.
Deployment
Local Development: The project is configured to run on a local development environment for frontend (localhost:3000) and backend (localhost:5000).
