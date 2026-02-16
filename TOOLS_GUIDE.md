# Tools Guide

> **Inspiration & Credit**: This guide is directly inspired by [Simon Willison's TOOLS_GUIDE.md](https://github.com/simonw/tools/blob/main/TOOLS_GUIDE.md). If you're serious about building browser-based tools, **read Simon's guide first**—it's comprehensive, battle-tested across 200+ tools, and covers advanced patterns like WebAssembly, testing, and automation. This is a simplified version focused on getting started quickly.

A simple guide for creating new tools for this repository.

## Philosophy

Each tool is a **standalone HTML file** with embedded CSS and JavaScript. No build process required—just open it in a browser and it works. External JavaScript libraries via CDN (e.g., Chart.js, D3) are welcome when they simplify implementation.

## File Structure

```
tools-locallyoptimal/
├── index.html              # Main listing page
├── colophon.html          # About page
├── {tool-name}.html       # Individual tool files
└── README.md
```

## Creating a New Tool

### 1. File Naming

Name your tool file: `{tool-name}.html`

Examples:
- `json-formatter.html`
- `base64-encoder.html`
- `url-parser.html`

### 2. Basic HTML Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tool Name - Locally Optimal Tools</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            max-width: 900px;
            margin: 40px auto;
            padding: 0 20px;
            line-height: 1.6;
            color: #333;
        }

        h1 {
            border-bottom: 1px solid #eee;
            padding-bottom: 10px;
        }

        textarea, input[type="text"] {
            width: 100%;
            font-family: 'Monaco', 'Menlo', 'Courier New', monospace;
            font-size: 13px;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }

        button {
            background: #0366d6;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            margin-right: 10px;
        }

        button:hover {
            background: #0256c7;
        }

        .error {
            color: #d73a49;
            background: #ffeef0;
            padding: 10px;
            border-radius: 4px;
            display: none;
        }

        footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            font-size: 0.9em;
            color: #586069;
        }

        footer a {
            color: #0366d6;
        }

        /* Mobile-friendly */
        @media (max-width: 600px) {
            body {
                padding: 10px;
            }
            h1 {
                font-size: 24px;
            }
        }
    </style>
</head>
<body>
    <h1>Tool Name</h1>
    <p>Brief description of what this tool does</p>

    <div id="error" class="error"></div>

    <!-- Your tool UI goes here -->
    <textarea id="input" placeholder="Enter text..."></textarea>

    <button onclick="processInput()">Process</button>
    <button onclick="clearInput()">Clear</button>

    <footer>
        <p><a href="index.html">← Back to tools</a></p>
    </footer>

    <script>
        function showError(message) {
            const errorDiv = document.getElementById('error');
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
        }

        function hideError() {
            document.getElementById('error').style.display = 'none';
        }

        function processInput() {
            hideError();
            const input = document.getElementById('input').value;

            try {
                // Your processing logic here

            } catch (e) {
                showError('Error: ' + e.message);
            }
        }

        function clearInput() {
            document.getElementById('input').value = '';
            hideError();
        }
    </script>
</body>
</html>
```

### 3. Common Patterns

#### Copy to Clipboard

```javascript
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        // Optional: show success feedback
    } catch (err) {
        showError('Failed to copy: ' + err.message);
    }
}
```

#### Real-time Processing

```javascript
const input = document.getElementById('input');
input.addEventListener('input', function() {
    // Process as user types
    const result = processData(input.value);
    document.getElementById('output').value = result;
});
```

#### File Upload

```javascript
const fileInput = document.getElementById('file-input');
fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.onload = (event) => {
        processFile(event.target.result);
    };
    reader.readAsText(file); // or readAsDataURL() for images
});
```

### 4. Design Guidelines

- **Max-width**: 800-900px centered container
- **Mobile-first**: Include viewport meta tag
- **Responsive**: Add mobile breakpoint around 600px
- **Consistent styling**: Match existing tools' look and feel
- **Footer**: Always include link back to index

### 5. Adding to Index

After creating your tool, add it to `index.html`:

```html
<li class="tool-item">
    <h3><a href="your-tool.html">Your Tool Name</a></h3>
    <p>Brief description of what it does</p>
</li>
```

## Development Workflow

1. **Create** the HTML file
2. **Test** locally by opening in browser
3. **Add** to `index.html`
4. **Commit** with descriptive message
5. **Push** - GitHub Pages auto-deploys

## Local Testing

No server needed—just open the HTML file in your browser:

```bash
open json-formatter.html
# or
python3 -m http.server 8000
# then visit http://localhost:8000/
```

## Examples

Look at existing tools for reference:
- `json-formatter.html` - Simple input/output processing
- `base64-encoder.html` - Multiple inputs with error handling

## Checklist for New Tools

- [ ] Mobile-responsive viewport meta tag
- [ ] Max-width centered layout
- [ ] Error handling with user feedback
- [ ] Clear button to reset state
- [ ] Footer link back to index
- [ ] Works without internet (CDN libraries are fine, but no server-side dependencies)
- [ ] Added to `index.html`
- [ ] Tested on mobile
