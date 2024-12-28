import React from "react";
import AddFoodForm from "./components/AddFoodForm";
import FoodTable from "./components/FoodTable";
import "./styles/App.css";

const App = () => {
  return (
    <div className="app">
      <h1>SmartShelf - Food Expiration Tracker</h1>
      <AddFoodForm />
      <FoodTable />
    </div>
  );
};

export default App;
