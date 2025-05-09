const express = require('express');
const router = express.Router();
const { render } = require('ejs');
const {ensureAuthenticated, ensureGuest} = require('../middleware/auth')


router.get("/", ensureGuest, async (req, res) => {
    try {
        res.render('home', {
            title: 'pdfGen',
        });
    } catch (err) {
        res.json({
            message: err.message,
        });
    }
});

// Export the router
module.exports = router;  // Make sure you're exporting the router object
