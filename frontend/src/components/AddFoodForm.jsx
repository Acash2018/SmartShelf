import React, { useState } from "react";
import axios from "../services/api";
import "../styles/components.css"; // Import the CSS file

const AddFoodForm = () => {
  const [name, setName] = useState("");
  const [expirationDate, setExpirationDate] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    await axios.post("/add_food", { name, expiration_date: expirationDate });
    setName("");
    setExpirationDate("");
  };

  return (
    <form onSubmit={handleSubmit}>
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
