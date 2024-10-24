import { EditorState, EditorView, basicSetup } from "@codemirror/basic-setup"
import { javascript } from "@codemirror/lang-javascript"
import { html } from "@codemirror/lang-html"
import { oneDark } from "@codemirror/theme-one-dark"

// Initialize CodeMirror
let editor = new EditorView({
    state: EditorState.create({
        extensions: [
            basicSetup,
            html(),
            javascript(),
            oneDark,
            EditorView.theme({
                "&": {
                    height: "100%",
                    fontSize: "14px"
                },
                ".cm-scroller": {
                    overflow: "auto"
                },
                ".cm-content": {
                    whiteSpace: "pre-wrap"
                }
            }),
            EditorView.updateListener.of(update => {
                if (update.docChanged) {
                    // Handle content changes here
                    handleEditorChange(update.state.doc.toString());
                }
            })
        ]
    }),
    parent: document.getElementById("codeEditor")
});

function handleEditorChange(content) {
    // Debounce the preview update
    clearTimeout(window.previewTimeout);
    window.previewTimeout = setTimeout(() => {
        updatePDFPreview(content);
    }, 1000);
}

async function updatePDFPreview(content) {
    try {
        const previewLoader = document.getElementById('previewLoader');
        if (previewLoader) previewLoader.classList.remove('hidden');

        // Send content to server for PDF generation
        const response = await fetch('/generate-pdf', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ content })
        });

        if (!response.ok) throw new Error('PDF generation failed');

        // Update the preview
        const pdfPreview = document.getElementById('pdfPreview');
        pdfPreview.src = `/view-pdf/preview?t=${Date.now()}`; // Cache busting
    } catch (error) {
        console.error('Preview update failed:', error);
        // Show error notification using DaisyUI
        showNotification('Preview update failed', 'error');
    } finally {
        if (previewLoader) previewLoader.classList.add('hidden');
    }
}

function showNotification(message, type = 'info') {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} fixed top-4 right-4 w-96 z-50`;
    alert.innerHTML = `
        <span>${message}</span>
        <button onclick="this.parentElement.remove()" class="btn btn-ghost btn-sm">✕</button>
    `;
    document.body.appendChild(alert);
    setTimeout(() => alert.remove(), 5000);
}

export { editor };