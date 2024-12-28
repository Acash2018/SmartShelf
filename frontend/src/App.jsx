import React, { useEffect, useState } from "react";
import FoodTable from "./components/FoodTable";
import "./index.css";
import axios from "./services/api";

const App = () => {
  const [foodList, setFoodList] = useState([]);

  const fetchFoodItems = async () => {
    try {
        const response = await axios.get("/food_items");
        setFoodList(response.data.food_items); // Update the food list
      } catch (error) {
        console.error("Error fetching food items:", error);
      }
  };

  const deleteFoodItem = async (id) => {
    await axios.delete(`/delete_food/${id}`);
    fetchFoodItems(); // Refresh the table after deletion
  };

  useEffect(() => {
    fetchFoodItems();
  }, []);

  return (
    <div className="app">
      <h1>SmartShelf - Food Expiration Tracker</h1>
      <AddFoodForm refreshFoodList={fetchFoodItems} />
      <FoodTable foodList={foodList} deleteFood={deleteFoodItem} />
    </div>
  );
};

export default App;
