import axios from "axios";

const API_BASE = "http://localhost:5000/api";

export const predictPrice = async (data) => {
  const response = await axios.post(
    `${API_BASE}/valuation`,
    data
  );

  return response.data;
};
