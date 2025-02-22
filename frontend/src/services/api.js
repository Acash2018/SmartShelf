import axios from "axios";

export const deleteFoodItem = async (id) => {
  try {
    const response = await axios.delete(`/delete_food/${id}`);
    return response.data;
  } catch (error) {
    console.error("Error deleting food item:", error);
    throw error;
  }
};

const instance = axios.create({
  baseURL: "http://127.0.0.1:5000", // Backend URL
});
export default instance;

