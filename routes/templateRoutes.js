const express = require('express');
const passport = require('passport');
const router = express.Router();

router.get("/", async (req, res) => {
    try {
        res.render('templates', {
            title: 'pdfGen | Templates',
        });
    } catch (err) {
        res.json({
            message: err.message,
        });
    }
});

module.exports = router;