const express = require('express');
const passport = require('passport');
const router = express.Router();
const {ensureAuthenticated, ensureGuest} = require('../middleware/auth')

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