import React, { useEffect, useState } from "react";
import FoodTable from "./components/FoodTable";
import axios from "./services/api";

const App = () => {
  const [foodList, setFoodList] = useState([]);

  const fetchFoodItems = async () => {
    const response = await axios.get("/food_items");
    setFoodList(response.data.food_items);
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
      <FoodTable foodList={foodList} deleteFood={deleteFoodItem} />
    </div>
  );
};

export default App;
