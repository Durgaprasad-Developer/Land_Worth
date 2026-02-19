const express = require("express");
const cors = require("cors");

const valuationRoutes = require("./routes/valuation.routes");
const errorMiddleware = require("./middlewares/error.middleware");

const app = express();

app.use(cors());
app.use(express.json());

app.use("/api/valuation", valuationRoutes);

app.use(errorMiddleware);

module.exports = app;
