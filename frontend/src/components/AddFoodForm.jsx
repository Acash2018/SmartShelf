import React, { useState } from "react";
import axios from "../services/api";

const AddFoodForm = ({ refreshFoodList }) => {
  const [name, setName] = useState("");
  const [expirationDate, setExpirationDate] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post("/add_food", { name, expiration_date: expirationDate });
      setName("");
      setExpirationDate("");
      refreshFoodList(); // Refresh the table after adding
    } catch (error) {
      console.error("Error adding food:", error);
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
