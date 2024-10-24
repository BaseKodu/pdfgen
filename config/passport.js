const passport = require('passport');
const GoogleStrategy = require('passport-google-oauth20').Strategy;
const User = require('../models/user')


passport.use(
  new GoogleStrategy(
    {
      clientID: process.env.google_client_id,
      clientSecret: process.env.google_client_secret,
      callbackURL: "http://localhost:3000/auth/google/callback",
      userProfileURL: "https://www.googleapis.com/oauth2/v3/userinfo"
    },
    async function(accessToken, refreshToken, profile, cb) {
      try {
        // Check if user already exists
        let user = await User.findOne({ googleId: profile.id });
        
        if (user) {
          // Update last login if user exists
          user.lastLogin = new Date();
          await user.save();
        } else {
          // Create new user if they don't exist
          user = await User.create({
            googleId: profile.id,
            email: profile.emails[0].value,
            displayName: profile.displayName,
            firstName: profile.name.givenName,
            lastName: profile.name.familyName,
            profilePhoto: profile.photos[0].value,
            lastLogin: new Date()
          });
        }
        
        return cb(null, user);
      } catch (err) {
        return cb(err, null);
      }
    }
));

passport.serializeUser((user, done) => {
  done(null, user.id);
});

passport.deserializeUser(async (id, done) => {
  try {
    const user = await User.findById(id);
    done(null, user);
  } catch (err) {
    done(err, null);
  }
});
