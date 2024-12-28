import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App"; // Ensure App.jsx exists in the same folder
import "./index.css"; // Optional, for global styles

// Render the App component into the root div in public/index.html
const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
