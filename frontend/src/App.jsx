import React, { useEffect, useState } from "react";

import AddFoodForm from './components/AddFoodForm';
import FoodTable from "./components/FoodTable";
import "./index.css";
import axios from "./services/api";

const App = () => {
  const [foodList, setFoodList] = useState([]);

  // Fetch food items from the backend
  const fetchFoodItems = async () => {
    try {
      const response = await axios.get("/food_items");
      setFoodList(response.data.food_items); // Update the food list
    } catch (error) {
      console.error("Error fetching food items:", error);
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
    </div>
  );
};

export default App;
