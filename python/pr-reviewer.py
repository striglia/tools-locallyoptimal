#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
PR Reviewer - AI-powered GitHub PR code review using Claude Code.

Run from within a cloned git repository:
    uv run https://tools.locallyoptimal.com/python/pr-reviewer.py 123

Or locally:
    python3 pr-reviewer.py 123
"""

import argparse
import shutil
import subprocess
import sys

# Maximum diff lines before we refuse to review (prevents context overflow)
MAX_DIFF_LINES = 50000

DEFAULT_PROMPT = """You are a careful, experienced senior software engineer conducting a thorough code review.
Your goal is to provide educational, informative feedback that helps developers understand
not just WHAT issues exist, but WHY they matter and HOW to fix them.

**SCOPE BOUNDARIES:**
Only review files that were actually changed in this PR.
- Do NOT comment on code in unchanged files
- Match your review scope to the PR scope

**Review Style:**
- Be thorough but constructive - explain the reasoning behind each concern
- Categorize issues by severity: Critical, Important, Suggestion
- Acknowledge what's done well
- Include file paths and line numbers for all references

**Focus Areas (in priority order):**
1. **Security** - XSS, injection attacks, command injection, unsafe patterns
2. **Correctness** - Logic errors, edge cases, data validation, error handling
3. **Business Value** - Future extensibility, maintainability, technical debt
4. **Non-Functional** - Performance, accessibility, code quality

**Output Format:**
For each issue, provide:
- Severity level (Critical/Important/Suggestion)
- Clear title of the issue
- WHY this matters (impact/risk)
- WHERE it occurs (file:line)
- HOW to fix it (with code example if helpful)

End with:
1. "Positive Notes" section highlighting what was done well
2. Overall recommendation: APPROVE, REQUEST_CHANGES, or COMMENT
"""


def check_dependencies() -> None:
    """Verify required CLI tools are installed."""
    deps = [
        ("claude", "npm install -g @anthropic-ai/claude-code"),
        ("gh", "https://cli.github.com/"),
    ]

    for cmd, install_msg in deps:
        if shutil.which(cmd) is None:
            print(f"Error: '{cmd}' not found.", file=sys.stderr)
            print(f"Install: {install_msg}", file=sys.stderr)
            sys.exit(1)


def get_repo_info() -> tuple[str, str]:
    """Get owner/repo from current git repository using gh."""
    try:
        result = subprocess.run(
            ["gh", "repo", "view", "--json", "owner,name", "-q", ".owner.login + \"/\" + .name"],
            capture_output=True,
            text=True,
            check=True,
        )
        repo = result.stdout.strip()
        if "/" not in repo:
            print("Error: Could not determine repository from current directory.", file=sys.stderr)
            print("Make sure you're in a git repository with a GitHub remote.", file=sys.stderr)
            sys.exit(1)
        owner, name = repo.split("/", 1)
        return owner, name
    except subprocess.CalledProcessError as e:
        print("Error: Could not get repository info.", file=sys.stderr)
        print("Make sure you're in a git repository with a GitHub remote.", file=sys.stderr)
        if e.stderr:
            print(e.stderr, file=sys.stderr)
        sys.exit(1)


def fetch_pr_diff(pr_number: int) -> str:
    """Fetch the diff for a PR using gh."""
    try:
        result = subprocess.run(
            ["gh", "pr", "diff", str(pr_number)],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error: Could not fetch PR #{pr_number}.", file=sys.stderr)
        if "Could not resolve" in (e.stderr or ""):
            print(f"PR #{pr_number} not found.", file=sys.stderr)
        elif e.stderr:
            print(e.stderr, file=sys.stderr)
        sys.exit(1)


def validate_diff_size(diff: str) -> None:
    """Check if diff is too large for review."""
    line_count = diff.count("\n")
    if line_count > MAX_DIFF_LINES:
        print(f"Error: PR diff is {line_count:,} lines.", file=sys.stderr)
        print(f"Maximum supported is {MAX_DIFF_LINES:,} lines.", file=sys.stderr)
        print("Consider breaking this PR into smaller pieces for review.", file=sys.stderr)
        sys.exit(1)


def build_prompt(diff: str, custom_prompt: str | None = None) -> str:
    """Build the full prompt for Claude."""
    prompt_parts = [DEFAULT_PROMPT]

    if custom_prompt:
        prompt_parts.append(f"\n**Additional Instructions:**\n{custom_prompt}")

    prompt_parts.append(f"\n<diff>\n{diff}\n</diff>")

    return "\n".join(prompt_parts)


def run_claude(prompt: str, model: str | None = None) -> str:
    """Run Claude Code in headless mode and return the response."""
    cmd = ["claude", "-p", prompt, "--allowedTools", "Read,Glob,Grep"]

    if model:
        cmd.extend(["--model", model])

    print("Running Claude Code review... (this may take a few minutes)")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
        )

        if result.returncode != 0:
            print("Error: Claude returned an error.", file=sys.stderr)
            if result.stderr:
                print(result.stderr, file=sys.stderr)
            sys.exit(1)

        return result.stdout
    except subprocess.TimeoutExpired:
        print("Error: Claude timed out after 5 minutes.", file=sys.stderr)
        print("Try running with --dry-run to debug, or break into smaller PRs.", file=sys.stderr)
        sys.exit(1)


def display_review(review: str) -> None:
    """Display the review to the user."""
    print("\n" + "=" * 70)
    print("CLAUDE CODE REVIEW")
    print("=" * 70)
    print(review)
    print("=" * 70)


def confirm_action() -> str | None:
    """Prompt user to confirm review action. Returns 'approve', 'request_changes', 'comment', or None."""
    print("\nHow would you like to proceed?")
    print("  [A] Approve")
    print("  [R] Request changes")
    print("  [C] Comment (no approval status)")
    print("  [X] Cancel (don't post)")

    while True:
        try:
            choice = input("\nChoice [A/R/C/X]: ").strip().upper()
        except (EOFError, KeyboardInterrupt):
            print("\nCancelled.")
            return None

        if choice == "A":
            return "approve"
        elif choice == "R":
            return "request_changes"
        elif choice == "C":
            return "comment"
        elif choice == "X":
            return None
        else:
            print("Invalid choice. Please enter A, R, C, or X.")


def post_review(pr_number: int, review: str, action: str) -> None:
    """Post the review to GitHub using gh pr review."""
    # Map action to gh pr review flags
    action_flags = {
        "approve": ["--approve"],
        "request_changes": ["--request-changes"],
        "comment": ["--comment"],
    }

    flags = action_flags.get(action, ["--comment"])

    try:
        subprocess.run(
            ["gh", "pr", "review", str(pr_number), *flags, "--body", review],
            check=True,
        )
        print(f"\nReview posted successfully to PR #{pr_number}!")
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to post review to PR #{pr_number}.", file=sys.stderr)
        if e.stderr:
            print(e.stderr, file=sys.stderr)
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="AI-powered GitHub PR code review using Claude Code.",
        epilog="Run from within a cloned git repository.",
    )
    parser.add_argument(
        "pr_number",
        type=int,
        help="PR number to review",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show review but don't post to GitHub",
    )
    parser.add_argument(
        "--model",
        type=str,
        choices=["sonnet", "opus", "haiku"],
        help="Claude model to use (default: sonnet)",
    )
    parser.add_argument(
        "--prompt",
        type=str,
        help="Additional instructions for the review",
    )

    args = parser.parse_args()

    # Check dependencies
    check_dependencies()

    # Get repo info
    owner, repo = get_repo_info()
    print(f"Reviewing PR #{args.pr_number} in {owner}/{repo}")

    # Fetch diff
    diff = fetch_pr_diff(args.pr_number)
    if not diff.strip():
        print("Error: PR has no diff (empty or already merged?).", file=sys.stderr)
        sys.exit(1)

    # Validate size
    validate_diff_size(diff)

    # Build prompt
    prompt = build_prompt(diff, args.prompt)

    # Run Claude
    review = run_claude(prompt, args.model)

    # Display review
    display_review(review)

    # Handle dry run
    if args.dry_run:
        print("\n[Dry run - not posting to GitHub]")
        return

    # Confirm and post
    action = confirm_action()
    if action is None:
        print("Review cancelled.")
        return

    post_review(args.pr_number, review, action)


if __name__ == "__main__":
    main()
