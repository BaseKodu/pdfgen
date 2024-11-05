const express = require('express');
const passport = require('passport');
const router = express.Router();
const {ensureAuthenticated, ensureGuest} = require('../middleware/auth')
const Template = require('../models/template')

router.get("/", ensureAuthenticated, async (req, res) => {
    try {
        const userTemplates = await Template.find({ user: req.user._id });

        // Rendering the 'templates' view with the correct data
        res.render('pages/templates', {
            title: 'pdfGen | Templates',
            templates: userTemplates,
            showTemplates: true,  // This enables the template list in sidebar
            hideSidebar: false 
        });
    } catch (err) {
        res.json({
            message: err.message,
            type: "danger"
        });
    }
});

router.post('/add-template', ensureAuthenticated, async (req, res) =>{
    try{
        const formdata = req.body;
        const newTemplate = new Template({
            title:req.body.title,
            description:req.body.description,
            user:req.user._id,
        });
        await newTemplate.save();
        res.json({
            status: "success",
            message: "Template added successfully",
            type: "success"
        });
    } catch (err) {
        res.json({
            message: err.message,
            type: "danger"
        });
    }
});


router.get('/edit', ensureAuthenticated, async (req, res) => {
    try{
        const template = await Template.findById(req.params.id);
        res.render('template_edit', {
            title: 'pdfGen | Edit Template',
            template: template
        });
    } catch (err) {
        res.json({
            message: err.message,
            type: "danger"
        });
    }
});


module.exports = router;