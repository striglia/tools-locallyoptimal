# Python Scripts

Standalone Python scripts that can be run via `uv run` directly from URLs.

## Prerequisites

These scripts require:
- **Python 3.10+** (installed with [uv](https://docs.astral.sh/uv/))
- **gh** - GitHub CLI ([install](https://cli.github.com/))
- **claude** - Claude Code CLI (`npm install -g @anthropic-ai/claude-code`)

## Available Scripts

### pr-reviewer.py

AI-powered GitHub PR code review using Claude Code in headless mode.

**Usage:**

```bash
# Run from within a cloned git repository
cd your-repo

# Review PR #123
uv run https://tools.locallyoptimal.com/python/pr-reviewer.py 123

# With custom instructions
uv run https://tools.locallyoptimal.com/python/pr-reviewer.py 123 --prompt "Focus on security"

# Dry run (show review, don't post)
uv run https://tools.locallyoptimal.com/python/pr-reviewer.py 123 --dry-run

# Use a specific Claude model
uv run https://tools.locallyoptimal.com/python/pr-reviewer.py 123 --model opus
```

**Options:**
- `--dry-run` - Display the review without posting to GitHub
- `--model {sonnet,opus,haiku}` - Choose Claude model (default: sonnet)
- `--prompt TEXT` - Add custom review instructions

**What it does:**
1. Fetches the PR diff from GitHub
2. Sends it to Claude Code with an opinionated code review prompt
3. Shows you the review and asks for confirmation
4. Posts the review to GitHub (approve, request changes, or comment)

**Review Focus Areas:**
1. Security - XSS, injection attacks, command injection
2. Correctness - Logic errors, edge cases, error handling
3. Business Value - Extensibility, maintainability
4. Non-Functional - Performance, accessibility, code quality

## Running Locally

You can also clone the repo and run scripts directly:

```bash
git clone https://github.com/striglia/tools-locallyoptimal.git
cd tools-locallyoptimal/python
python3 pr-reviewer.py 123
```

## Adding New Scripts

New Python scripts should follow this pattern:

```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Script description."""

# Your code here
```

The `# /// script` block enables `uv run` to automatically handle Python version and dependencies.
