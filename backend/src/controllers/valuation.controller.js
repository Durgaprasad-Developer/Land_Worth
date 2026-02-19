const { getValuation } = require("../services/ml.service");
const { isInsideVijayawada } = require("../utils/boundary.util");

exports.predict = async (req, res, next) => {
  try {
    const { latitude, longitude, classification } = req.body;

    if (!isInsideVijayawada(latitude, longitude)) {
      return res.status(400).json({
        error: "Location outside Vijayawada boundary"
      });
    }

    const result = await getValuation({
      latitude,
      longitude,
      classification
    });

    res.json(result);

  } catch (err) {
    next(err);
  }
};
