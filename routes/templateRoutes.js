const express = require('express');
const passport = require('passport');
const router = express.Router();
const {ensureAuthenticated, ensureGuest} = require('../middleware/auth')
const Template = require('../models/template')

router.get("/", ensureAuthenticated, async (req, res) => {
    try {
        const userTemplates = await Template.find({ user: req.user._id });

        // Rendering the 'templates' view with the correct data
        res.render('templates', {
            title: 'pdfGen | Templates',
            templates: userTemplates // Passing the correct variable here

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


router.get('/edit/:id', ensureAuthenticated, async (req, res) => {
    try {
        const template = await Template.findById(req.params.id);
        if (!template) {
            return res.status(404).json({
                message: "Template not found",
                type: "danger"
            });
        }
        res.render('template_edit', {
            title: 'pdfGen | Edit Template',
            template: template
        });
    } catch (err) {
        res.status(500).json({
            message: err.message,
            type: "danger"
        });
    }
});


// Route to update template
router.post('/templates/update/:id', ensureAuthenticated, async (req, res) => {
    try {
        const template = await Template.findByIdAndUpdate(
            req.params.id,
            { content: req.body.content },
            { new: true }
        );
        res.json({ type: 'success', message: 'Template updated successfully' });
    } catch (err) {
        res.status(500).json({ type: 'danger', message: err.message });
    }
});

// Route to generate preview
router.post('/templates/preview', ensureAuthenticated, async (req, res) => {
    try {
        // Here you'll implement your PDF generation logic
        // Store the preview temporarily
        // You might want to use something like pdf-lib or puppeteer
        res.json({ type: 'success' });
    } catch (err) {
        res.status(500).json({ type: 'danger', message: err.message });
    }
});

// Route to serve preview PDF
router.get('/templates/preview-pdf', ensureAuthenticated, (req, res) => {
    // Serve the temporarily generated preview PDF
    // Implementation depends on how you're generating/storing the preview
});


module.exports = router;