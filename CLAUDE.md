# Tools - Locally Optimal

Project-specific instructions for Claude Code when working on this repository.

## Project Overview

This is a collection of small, single-purpose browser tools inspired by [Simon Willison's tools](https://tools.simonwillison.net/). Each tool is a standalone HTML file with embedded CSS and JavaScript - no build process, no dependencies, just open and use.

**Target audience**: SF-based, high-income dual-earner households (tech + professional backgrounds) looking for practical financial and productivity tools.

## Workflow Rules

### Git Workflow
- **ALWAYS use feature branches** - Use the `/git-workflow` skill or manual feature branches
- **NEVER commit directly to main** - All changes should go through pull requests
- **Reference GitHub issues** - Link commits and PRs to issue numbers
- **Use conventional commits** - Clear, descriptive commit messages

### Branch Naming
- `feature/issue-N-short-description` for new features
- `fix/issue-N-short-description` for bug fixes
- Example: `feature/issue-6-529-calculator`

## Adding New Tools

### Process
1. **Create GitHub issue** describing the tool (inputs, outputs, technical requirements)
2. **Read TOOLS_GUIDE.md** for the technical template and patterns
3. **Create the tool HTML file** following existing patterns
4. **Update index.html** - Add tool to the list with name and description
5. **Update colophon.html** - Add tool to the tools list
6. **Test locally** - Open the HTML file in a browser, test all functionality
7. **Create PR via `/git-workflow`** - Feature branch → commits → pull request

### File Locations
- Tool files: `{tool-name}.html` in root directory
- Update: `index.html` (add to tools list)
- Update: `colophon.html` (add to tools list)

### Tool Standards
All tools must follow these requirements:

#### Architecture
- ✅ Single standalone HTML file with embedded CSS and JavaScript
- ✅ No external dependencies (no CDNs, no frameworks)
- ✅ All processing happens client-side (no server calls)
- ✅ Works offline after first load

#### Design
- ✅ Mobile-responsive (viewport meta tag + responsive CSS)
- ✅ Max-width 800-900px centered container
- ✅ Consistent styling with existing tools (see TOOLS_GUIDE.md)
- ✅ System fonts: `-apple-system, BlinkMacSystemFont, "Segoe UI"...`
- ✅ Color scheme matches existing tools
- ✅ Footer with "← Back to tools" link

#### Functionality
- ✅ Clear error handling with user feedback
- ✅ Input validation
- ✅ Clear/reset functionality
- ✅ Keyboard shortcuts where appropriate (Enter to submit, etc.)
- ✅ Real-time updates preferred over button clicks (where appropriate)

#### Code Quality
- ✅ Clean, readable JavaScript
- ✅ Comments for complex logic
- ✅ Proper event handling (no memory leaks)
- ✅ Accessible HTML (semantic elements, labels, ARIA where needed)

## Testing Tools

### Local Testing
```bash
# Option 1: Direct open
open tool-name.html

# Option 2: Local server
python3 -m http.server 8000
# Then visit http://localhost:8000/tool-name.html
```

### Test Checklist
- [ ] Tool loads without errors
- [ ] All inputs accept valid data
- [ ] Invalid data shows appropriate errors
- [ ] Calculations/transformations are accurate
- [ ] Clear button resets to defaults
- [ ] Mobile responsive (test at 600px, 375px widths)
- [ ] Works in Chrome, Firefox, Safari
- [ ] No console errors or warnings
- [ ] Footer link returns to index

### Testing Complex Tools
For tools with calculations (like 529 calculator):
- Verify against external calculators/references
- Test edge cases (zero values, negative numbers, etc.)
- Validate formulas with citations
- Test with realistic user scenarios

## Code Patterns

### Standard Template Structure
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tool Name - Locally Optimal Tools</title>
    <style>
        /* Embedded CSS - see TOOLS_GUIDE.md for standard styles */
    </style>
</head>
<body>
    <h1>Tool Name</h1>
    <p>Description</p>

    <!-- Inputs -->
    <!-- Controls -->
    <!-- Results -->

    <footer>
        <p><a href="index.html">← Back to tools</a></p>
    </footer>

    <script>
        // Embedded JavaScript
    </script>
</body>
</html>
```

### Common Patterns
See TOOLS_GUIDE.md for:
- Copy to clipboard
- Real-time processing
- File upload
- Error handling
- Input validation

## Deployment

### GitHub Pages
- Automatic deployment on push to main
- Custom domain: tools.locallyoptimal.com (via CNAME)
- No build process needed - HTML files are served directly

### Pre-deployment Checklist
- [ ] All tests pass locally
- [ ] index.html updated with new tool
- [ ] colophon.html updated with new tool
- [ ] PR reviewed and approved
- [ ] Commits are clean and descriptive

## Future Enhancements

### Planned Improvements (Issue #10)
- Auto-generate index.html from tool files (like Simon Willison)
- Auto-generate colophon.html from tool files
- Build scripts + GitHub Actions workflow
- Reduces manual updates when adding tools

### Skill Ideas
- `/create-tool` - Automate tool creation boilerplate
- `/test-tool-browser` - Playwright-based visual testing

## References

- **Main inspiration**: [Simon Willison's tools](https://tools.simonwillison.net/) and [his TOOLS_GUIDE.md](https://github.com/simonw/tools/blob/main/TOOLS_GUIDE.md)
- **IWT calculator**: https://www.iwillteachyoutoberich.com/investment-calculator/
- **GitHub repo**: https://github.com/striglia/tools-locallyoptimal
- **Live site**: https://tools.locallyoptimal.com
- **Main blog**: http://locallyoptimal.com

## Philosophy

> "Makes abstract concepts concrete through simple, focused tools. Each tool does one thing well. No unnecessary complexity, no external dependencies, just helpful calculations that run entirely in your browser."

Focus on tools that are:
- **Practical** - Solve real problems for the target audience
- **Simple** - No learning curve, obvious how to use
- **Fast** - Instant feedback, no loading states
- **Private** - All calculations client-side, no data sent anywhere
- **Permanent** - Works offline, no API dependencies to break
