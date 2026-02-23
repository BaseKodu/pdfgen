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
    let autoSaveEnabled = false;
    let autoSaveInterval;
    const LOCAL_STORAGE_KEY = `template_${templateId}`;
    const AUTO_SAVE_INTERVAL = 30000; // 30 seconds

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
        height: "100%",
        viewportMargin: Infinity,
        extraKeys: {
            "Ctrl-S": function(cm) {
                saveTemplate();
            }
        }
    });

    // Set editor size
    editor.setSize("100%", "100%");

    // Load from local storage if available
    const savedContent = localStorage.getItem(LOCAL_STORAGE_KEY);
    if (savedContent) {
        const shouldRestore = confirm("Found unsaved changes. Would you like to restore them?");
        if (shouldRestore) {
            editor.setValue(savedContent);
        } else {
            localStorage.removeItem(LOCAL_STORAGE_KEY);
        }
    }

    // Save to local storage
    function saveToLocalStorage() {
        const content = editor.getValue();
        localStorage.setItem(LOCAL_STORAGE_KEY, content);
    }

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
                // Clear local storage after successful save
                localStorage.removeItem(LOCAL_STORAGE_KEY);
                alert('Template saved successfully!');
                updatePDFPreview();
            } else {
                alert('Error saving template: ' + data.message);
            }
        } catch (err) {
            alert('Error saving template: ' + err.message);
            // Save to local storage in case of error
            saveToLocalStorage();
        }
    }

    // Toggle auto-save functionality
    const autoSaveToggle = document.getElementById('autoSaveToggle');
    autoSaveToggle.addEventListener('click', function() {
        autoSaveEnabled = !autoSaveEnabled;
        this.textContent = `Auto-save: ${autoSaveEnabled ? 'On' : 'Off'}`;
        
        if (autoSaveEnabled) {
            autoSaveInterval = setInterval(saveToLocalStorage, AUTO_SAVE_INTERVAL);
        } else {
            clearInterval(autoSaveInterval);
        }
    });

    // Save button click handler
    const saveButton = document.getElementById('saveButton');
    saveButton.addEventListener('click', saveTemplate);

    // Add debounced preview update and local storage save
    let previewTimeout;
    editor.on('change', function() {
        clearTimeout(previewTimeout);
        previewTimeout = setTimeout(() => {
            updatePDFPreview();
            saveToLocalStorage();
        }, 1000);
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

    // Handle beforeunload event to warn about unsaved changes
    window.addEventListener('beforeunload', function(e) {
        if (localStorage.getItem(LOCAL_STORAGE_KEY)) {
            e.preventDefault();
            e.returnValue = '';
        }
    });
});