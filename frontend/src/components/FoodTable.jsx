import React from "react";
import { deleteFoodItem } from "../services/api"; // Import the delete function from the API

const FoodTable = ({ foodList, refreshFoodList }) => {
  // Function to calculate the food item's status based on expiration date
  const calculateStatus = (expirationDate) => {
    const today = new Date();
    const expDate = new Date(expirationDate);
    const diffDays = Math.ceil((expDate - today) / (1000 * 60 * 60 * 24));

    if (diffDays < 0) return "Expired";
    if (diffDays <= 3) return "Expiring Soon";
    return "Fresh";
  };

  // Function to handle the delete action
  const handleDelete = async (id) => {
    try {
      await deleteFoodItem(id); // Call the backend API to delete the item
      refreshFoodList(); // Refresh the list of food items
    } catch (error) {
      alert("Failed to delete the food item. Please try again.");
    }
  };

  return (
    <div className="food-table">
      <h2>Food Items</h2>
      {foodList.length > 0 ? (
        <table>
          <thead>
            <tr>
              <th>Food Name</th>
              <th>Expiration Date</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {foodList.map((food) => (
              <tr key={food.id}>
                <td>{food.name}</td>
                <td>{food.expiration_date}</td>
                <td>{calculateStatus(food.expiration_date)}</td>
                <td>
                  <button onClick={() => handleDelete(food.id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No food items found.</p>
      )}
    </div>
  );
};

export default FoodTable;
