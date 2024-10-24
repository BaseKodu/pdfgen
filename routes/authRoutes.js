const express = require('express');
const passport = require('passport');
const router = express.Router();



// Initiates the Google OAuth 2.0 authentication flow
router.get('/google', passport.authenticate('google', { scope: ['profile', 'email'] }));

// Callback URL for handling the OAuth 2.0 response
router.get('/google/callback', 
  passport.authenticate('google', { 
    failureRedirect: '/',
    failureFlash: true // if you want to use flash messages
  }), 
  (req, res) => {
    res.redirect('/templates');
  }
);

// Logout route
router.get('/logout', (req, res) => {
  req.logout();
  res.redirect('/');
});

module.exports = router;
