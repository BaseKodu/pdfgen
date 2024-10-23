const passport = require('passport');
const GoogleStrategy = require('passport-google-oauth20').Strategy;
require('dotenv').config();


passport.use(
  new GoogleStrategy(
    {
      clientID: process.env.google_client_id,
      clientSecret: process.env.google_client_secret,
      callbackURL: "http://localhost:3000/auth/google/callback"
    },
    function(accessToken, refreshToken, profile, cb) {
      // Handle user authentication here
      // ...
    }
  )
);

passport.serializeUser((user, done) => {
  // Code to serialize user data
});

passport.deserializeUser((id, done) => {
  // Code to deserialize user data
});
