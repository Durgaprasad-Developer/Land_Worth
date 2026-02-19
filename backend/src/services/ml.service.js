const axios = require("axios");

const ML_SERVICE_URL = process.env.ML_SERVICE_URL || "http://127.0.0.1:8000";

async function getValuation(data) {
  const response = await axios.post(
    `${ML_SERVICE_URL}/predict-price`,
    data
  );

  return response.data;
}

module.exports = { getValuation };
