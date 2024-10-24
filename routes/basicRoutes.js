const express = require('express');
const router = express.Router();
const { render } = require('ejs');


router.get("/", async (req, res) => {
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
