// Import the express module
const express = require('express');

// Create an Express application
const app = express();

// Define a port
const port = 3000;

// Define a route (GET request to the root URL)
app.get('/', (req, res) => {
  res.send('Hello, world!');
});

// Start the server and listen on the defined port
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
