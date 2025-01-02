import React, { useEffect, useState } from "react";

import AddFoodForm from './components/AddFoodForm';
import FoodTable from "./components/FoodTable";
import "./index.css";
import axios from "./services/api";

const App = () => {
  const [foodList, setFoodList] = useState([]);
  const [email, setEmail] = useState("");

  // Fetch food items from the backend
  const fetchFoodItems = async () => {
    try {
      const response = await axios.get("/food_items");
      setFoodList(response.data.food_items); // Update the food list
    } catch (error) {
      console.error("Error fetching food items:", error);
    }
  };


  const sendEmail = async () => {
    try {
      if (!email) {
        alert("Please enter a valid email address.");
        return;
      }
      await axios.post("/send_email", { email });
      alert("Email sent successfully!");
    } catch (error) {
      console.error("Error sending email:", error);
      alert("Failed to send email. Please try again.");
    }
  };

  // Delete a food item
  const deleteFoodItem = async (id) => {
    try {
      await axios.delete(`/delete_food/${id}`);
      fetchFoodItems(); // Refresh the table after deletion
    } catch (error) {
      console.error("Error deleting food item:", error);
    }
  };

  // Fetch the food items on component mount
  useEffect(() => {
    fetchFoodItems();
  }, []);

  return (
    <div className="app">
      <h1>SmartShelf - Food Expiration Tracker</h1>
      <AddFoodForm refreshFoodList={fetchFoodItems} />
      <FoodTable foodList={foodList} deleteFood={deleteFoodItem} refreshFoodList={fetchFoodItems}/>
      <div className="email-section">
        <h2>Get Expiring Items via Email</h2>
        <input
          type="email"
          placeholder="Enter your email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <button onClick={sendEmail}>Send Email</button>
      </div>
    </div>
  );
};

export default App;
