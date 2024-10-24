const express = require('express');
const passport = require('passport');
const session = require('express-session');
const authRoutes = require('./routes/authRoutes');
const basicRoutes = require('./routes/basicRoutes');
const templateRoutes = require('./routes/templateRoutes')
const bodyParser = require('body-parser');
require('dotenv').config();

const app = express();

// Import Passport config
require('./config/passport');

// Middleware for sessions
app.use(express.urlencoded({extended:false}))
app.use(express.json())


app.use(session({
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: true
}));

// Initialize Passport and restore authentication state, if any, from the session
app.use(passport.initialize());
app.use(passport.session());

// View engine setup (optional, if you're using EJS or another templating engine)
app.set('view engine', 'ejs');

app.use('/', basicRoutes)
app.use('/templates', templateRoutes)
app.use('/auth', authRoutes)


app.use(express.static('public'));


// Start the server
const port = 3000;
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
