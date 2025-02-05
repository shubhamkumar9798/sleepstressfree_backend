const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
const { spawn } = require("child_process"); // Import spawn from child_process

const app = express();
const port = 5000;

// Middleware
app.use(bodyParser.json());
app.use(cors());

// Health check route to confirm server is working
app.get("/", (req, res) => {
  res.send("Server is working");
});

// Define the prediction route
app.post("/predict", (req, res) => {
  // Extract the data sent from the frontend
  const {
    snoring_rate,
    respiration_rate,
    body_temperature,
    limb_movement,
    blood_oxygen,
    eye_movement,
    sleeping_hours,
    heart_rate,
  } = req.body;

  // Validate inputs: Ensure all fields are provided
  if (
    snoring_rate == null ||
    respiration_rate == null ||
    body_temperature == null ||
    limb_movement == null ||
    blood_oxygen == null ||
    eye_movement == null ||
    sleeping_hours == null ||
    heart_rate == null
  ) {
    return res.status(400).send({ error: "Missing input data" });
  }

  // Prepare the arguments for the Python script
  const args = [
    snoring_rate,
    respiration_rate,
    body_temperature,
    limb_movement,
    blood_oxygen,
    eye_movement,
    sleeping_hours,
    heart_rate,
  ];

  // Spawn a child process to run the Python script
  const pythonProcess = spawn("python", ["./predict_from_pkl.py", ...args]);

  let result = "";
  let error = "";

  // Collect data from the Python script's stdout
  pythonProcess.stdout.on("data", (data) => {
    result += data.toString();
  });

  // Collect errors from the Python script's stderr
  pythonProcess.stderr.on("data", (data) => {
    error += data.toString();
  });

  // Handle the Python script's exit
  pythonProcess.on("close", (code) => {
    if (code !== 0) {
      // If the Python script exits with a non-zero code, return an error
      console.error("Python script error:", error);
      return res.status(500).send({ error: "Prediction error: " + error });
    }

    if (result) {
      // The result is the output from the Python script
      res.json({ stress_level: result.trim() });
    } else {
      res.status(500).send({ error: "No prediction result returned from the model" });
    }
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});