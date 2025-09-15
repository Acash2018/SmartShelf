/* eslint-disable no-unused-vars */
import React, { useState } from "react";
import axios from "../services/api";


const AddFoodForm = ({ refreshFoodList }) => {
  const [name, setName] = useState("");
  const [expirationDate, setExpirationDate] = useState("");
  const [loading, setLoading] = useState(false);



   // 🔹 New: Predict expiration when name changes
  const handleNameChange = async (e) => {
    const foodName = e.target.value;
    setName(foodName);

    if (foodName.trim().length > 2) {
      try {
        const response = await axios.post("/predict_expiration", {
          food_name: foodName,
        });

        if (response.data.suggested_expiration) {
          setExpirationDate(response.data.suggested_expiration);
        }
      } catch (error) {
        console.error("Error predicting expiration:", error);
      }
      finally {
        setLoading(false);
      }
    
    }
  };

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
      {/* 🔹 Using handleNameChange */}
      <input
        type="text"
        placeholder="Food Name"
        value={name}
        onChange={handleNameChange} 
        required
      />
      <input
        type="date"
        value={expirationDate}
        onChange={(e) => setExpirationDate(e.target.value)}
        required
      />
      {loading && <p> Suggesting expiration...</p>}
      <button type="submit">Add Food</button>
    </form>
  );



};

export default AddFoodForm;
