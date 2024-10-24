// middleware/auth.js
const ensureAuthenticated = (req, res, next) => {
    if (req.isAuthenticated()) {
      return next();
    }
    res.redirect('/');
};
  
const ensureGuest = (req, res, next) => {
    if (!req.isAuthenticated()) {
        return next();
    }
    res.redirect('/templates'); // redirect if user is already logged in
};
  

  
module.exports = {
    ensureAuthenticated,
    ensureGuest,
};