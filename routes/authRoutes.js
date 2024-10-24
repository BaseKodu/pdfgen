const express = require('express');
const passport = require('passport');
const router = express.Router();
const {ensureAuthenticated, ensureGuest} = require('../middleware/auth')



// Initiates the Google OAuth 2.0 authentication flow
router.get('/google', ensureGuest, passport.authenticate('google', { scope: ['profile', 'email'] }));
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

// logout route
router.get('/logout',ensureAuthenticated, (req, res) => {
  req.logout((err) => {
    if (err) {
      console.error('Logout error:', err);
      return res.redirect('/');
    }
    res.redirect('/');
  });
});

module.exports = router;
