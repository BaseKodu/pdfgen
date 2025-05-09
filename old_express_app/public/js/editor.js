import CodeMirror from 'codemirror';
import 'codemirror/mode/xml/xml';
import 'codemirror/mode/javascript/javascript';
import 'codemirror/mode/css/css';
import 'codemirror/addon/edit/closetags';
import 'codemirror/addon/edit/closebrackets';
import 'codemirror/addon/mode/multiplex';
import 'codemirror/addon/mode/simple';

// Import required CSS
import 'codemirror/lib/codemirror.css';
import 'codemirror/theme/monokai.css';

// Define EJS mode
CodeMirror.defineMode("ejs", function(config, parserConfig) {
    return CodeMirror.multiplexingMode(
        CodeMirror.getMode(config, "text/html"), {
            open: "<%",
            close: "%>",
            mode: CodeMirror.getMode(config, "javascript"),
            delimStyle: "delimiter"
        }
    );
});

document.addEventListener('DOMContentLoaded', function() {
    const editor = CodeMirror.fromTextArea(document.getElementById("codeEditor"), {
        mode: "ejs",
        theme: "monokai",
        lineNumbers: true,
        autoCloseTags: true,
        autoCloseBrackets: true,
        lineWrapping: true,
        indentUnit: 2,
        tabSize: 2,
        autofocus: true,
        extraKeys: {
            "Ctrl-S": function(cm) {
                saveTemplate();
            }
        }
    });

    // Set editor size
    editor.setSize("100%", "100%");

    // Function to save template
    async function saveTemplate() {
        const content = editor.getValue();
        try {
            const response = await fetch(`/templates/update/${templateId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ content })
            });

            const data = await response.json();
            if (data.type === 'success') {
                alert('Template saved successfully!');
                updatePDFPreview();
            } else {
                alert('Error saving template: ' + data.message);
            }
        } catch (err) {
            alert('Error saving template: ' + err.message);
        }
    }

    // Add debounced preview update
    let previewTimeout;
    editor.on('change', function() {
        clearTimeout(previewTimeout);
        previewTimeout = setTimeout(updatePDFPreview, 1000);
    });

    async function updatePDFPreview() {
        const content = editor.getValue();
        try {
            const response = await fetch('/templates/preview', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ content })
            });
            
            if (response.ok) {
                const pdfPreview = document.getElementById('pdfPreview');
                pdfPreview.src = '/templates/preview-pdf?' + new Date().getTime();
            }
        } catch (err) {
            console.error('Error updating preview:', err);
        }
    }
});