import React from "react";
import "../styles/components.css"; // Import styles specific to the components

const FoodTable = ({ foodList, deleteFood }) => {
  // Function to calculate expiration status
  const calculateStatus = (expirationDate) => {
    const today = new Date();
    const expDate = new Date(expirationDate);
    const diffDays = Math.ceil((expDate - today) / (1000 * 60 * 60 * 24));

    if (diffDays < 0) return "Expired";
    if (diffDays <= 3) return "Expiring Soon";
    return "Fresh";
  };

  return (
    <div className="food-table-container">
      <table className="food-table">
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
              <td className={`status ${calculateStatus(food.expiration_date).toLowerCase()}`}>
                {calculateStatus(food.expiration_date)}
              </td>
              <td>
                <button onClick={() => deleteFood(food.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default FoodTable;
