const express = require('express');
const passport = require('passport');
const session = require('express-session');
const authRoutes = require('./routes/authRoutes');
const bodyParser = require('body-parser');
require('dotenv').config();
const app = express();

// Import Passport config
require('./config/passport');

// Middleware for sessions
app.use(session({
  secret: process.env.google_client_secret,
  resave: false,
  saveUninitialized: true
}));

// Initialize Passport and restore authentication state, if any, from the session
app.use(passport.initialize());
app.use(passport.session());

// View engine setup (optional, if you're using EJS or another templating engine)
app.set('view engine', 'ejs');

// Use the auth routes
app.use('/', authRoutes);

// Home route
app.get('/', (req, res) => {
  res.send('Welcome to the home page!');
});

// Login route
app.get('/login', (req, res) => {
  res.render('login');
});

// Start the server
const port = 3000;
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
