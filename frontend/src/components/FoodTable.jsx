import React from "react";

const FoodTable = ({ foodList, deleteFood }) => {
  const calculateStatus = (expirationDate) => {
    const today = new Date();
    const expDate = new Date(expirationDate);
    const diffDays = Math.ceil((expDate - today) / (1000 * 60 * 60 * 24));

    if (diffDays < 0) return "Expired";
    if (diffDays <= 3) return "Expiring Soon";
    return "Fresh";
  };

  return (
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
            <td>{calculateStatus(food.expiration_date)}</td>
            <td>
              {/* Delete Button */}
              <button onClick={() => deleteFood(food.id)}>Delete</button>
              
              {/* Debugging Delete Button */}
              <button
                onClick={() => {
                  console.log("Attempting to delete food with ID:", food.id);
                  deleteFood(food.id);
                }}
              >
                Debug Delete
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default FoodTable;
