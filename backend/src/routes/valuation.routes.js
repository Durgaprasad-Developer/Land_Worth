const express = require("express");
const router = express.Router();
const valuationController = require("../controllers/valuation.controller");

router.post("/", valuationController.predict);

module.exports = router;
