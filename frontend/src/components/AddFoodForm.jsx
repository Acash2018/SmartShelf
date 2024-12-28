import React, { useState } from "react";
import axios from "../services/api"; // Import the Axios instance

const AddFoodForm = ({ refreshFoodList }) => {
  const [name, setName] = useState("");
  const [expirationDate, setExpirationDate] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Send POST request to /add_food
      await axios.post("/add_food", {
        name: name.trim(),
        expiration_date: expirationDate, // Format: MM-DD-YYYY
      });

      // Clear form fields
      setName("");
      setExpirationDate("");

      // Refresh the food list
      refreshFoodList();
    } catch (error) {
      console.error("Error adding food item:", error);
      alert("Failed to add food item. Please try again.");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="add-food-form">
      <input
        type="text"
        placeholder="Food Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        required
      />
      <input
        type="date"
        value={expirationDate}
        onChange={(e) => setExpirationDate(e.target.value)}
        required
      />
      <button type="submit">Add Food</button>
    </form>
  );
};

export default AddFoodForm;
