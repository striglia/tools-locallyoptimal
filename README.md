# Tools - Locally Optimal

A collection of small, client-side tools hosted on GitHub Pages. Each tool runs entirely in your browser—no data is sent to any server.

Inspired by [Simon Willison's tools](https://tools.simonwillison.net/).

## Live Site

🚧 **Coming soon:** `tools.locallyoptimal.com` (pending GitHub Pages configuration)

## Current Tools

- **[JSON Formatter](json-formatter.html)** - Format and validate JSON with syntax highlighting
- **[Base64 Encoder/Decoder](base64-encoder.html)** - Encode and decode text to/from Base64

## Architecture

Each tool is a **standalone HTML file** with embedded JavaScript and CSS. This approach offers:

- ✅ No build process required
- ✅ No dependencies or frameworks
- ✅ Easy to add new tools (just add a new `.html` file)
- ✅ Works offline (after first load)
- ✅ Fast and simple

## Adding a New Tool

1. **Create a new HTML file** (e.g., `my-tool.html`) with this structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My Tool - Locally Optimal Tools</title>
    <style>
        /* Your CSS here */
    </style>
</head>
<body>
    <h1>My Tool</h1>
    <!-- Your UI here -->

    <script>
        // Your JavaScript here
    </script>
</body>
</html>
```

2. **Add it to `index.html`**:

```html
<li class="tool-item">
    <h3><a href="my-tool.html">My Tool</a></h3>
    <p>Brief description of what your tool does</p>
</li>
```

3. **Commit and push**—GitHub Pages will deploy automatically

## Project Structure

```
tools-locallyoptimal/
├── index.html              # Main landing page with tool list
├── colophon.html          # About page with technical details
├── json-formatter.html    # Tool: JSON formatter
├── base64-encoder.html    # Tool: Base64 encoder/decoder
└── README.md              # This file
```

## Development

### Local Testing

Just open `index.html` in your browser. No build step required.

### Deployment

Commits to `main` automatically deploy to GitHub Pages (once configured).

## GitHub Pages Setup

1. Go to repository Settings → Pages
2. Set source to "Deploy from a branch"
3. Select `main` branch, `/ (root)` folder
4. Optionally configure custom domain: `tools.locallyoptimal.com`

## Design Principles

- **Client-side only** - No server-side code; all tools run in the browser
- **No build process** - Plain HTML/CSS/JS; no webpack, no npm
- **Single-file tools** - Each tool is self-contained in one HTML file
- **Progressive enhancement** - Works without JavaScript where possible
- **Privacy-first** - No analytics, no tracking, no data collection

## Related

- Main blog: [locallyoptimal.com](http://locallyoptimal.com/)
- GitHub: [github.com/striglia/tools-locallyoptimal](https://github.com/striglia/tools-locallyoptimal)

## License

MIT (or whatever license you prefer)
