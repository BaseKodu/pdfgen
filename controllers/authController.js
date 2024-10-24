exports.loginPage = (req, res) => {
    res.render('login');
  };
  
  exports.logout = (req, res) => {
    req.logout();
    res.redirect('/');
  };
  