# Slack Text Cleaner

A standalone HTML tool that converts messy copy/pasted Slack conversations into clean, readable Markdown.

## Overview

When you copy text from Slack, you get a jumbled mess: emoji reactions with counts, image previews, inconsistent spacing, Slack-specific formatting, and various metadata. This tool cleans it up into proper Markdown suitable for documentation, sharing, or feeding into AI tools.

## Decisions Made

| Topic | Decision | Rationale |
|-------|----------|-----------|
| **Emojis** | Keep inline, remove reactions | Inline emojis are intentional content; reactions (👍 5) are metadata noise |
| **Formatting** | Convert to standard Markdown | `*bold*` → `**bold**`, `~strike~` → `~~strike~~` for universal compatibility |
| **Timestamps** | Optional toggle, OFF by default | Minimal output preferred, but timestamps useful for some contexts |
| **Threads** | Show indicator only | Thread content isn't in clipboard; display `[thread: N replies]` |
| **Image links** | Keep links, remove inlined images | URLs are useful; embedded image blobs are noise |
| **System messages** | Optional toggle, OFF by default | Join/leave/topic changes rarely needed |
| **Consecutive messages** | Repeat username each time | Cleaner with optional timestamps; easier to parse |
| **@mentions** | Keep as `@name` | Preserves context without extra formatting |
| **#channels** | Keep as `#channel` | Preserves context |
| **Code blocks** | Preserve exactly | Both ``` blocks and `inline` code kept as-is |
| **UX** | Real-time processing | Output updates as user pastes, no button needed |
| **Copy** | One-click copy button | Quick workflow with visual feedback |

## Functional Requirements

### Input
- Large textarea for pasting Slack conversation
- Accepts raw copy/pasted text from Slack desktop or web app

### Processing (real-time as user types/pastes)

**Always apply:**
1. Extract username from each message block → format as `@username: `
2. Remove emoji reactions (e.g., `:+1: 5`, `👍 3`, `:fire::heart: 12`)
3. Remove inline/embedded images (base64 blobs, Slack CDN image previews)
4. Convert Slack formatting to standard Markdown:
   - `*bold*` → `**bold**`
   - `~strikethrough~` → `~~strikethrough~~`
   - `_italic_` → `_italic_` (same)
   - Preserve code blocks and inline code
5. Normalize whitespace (collapse multiple blank lines to single)
6. Preserve regular links as `[text](url)` or raw URLs
7. Indicate threads as `[thread: N replies]`
8. Add blank line between each message

**Configurable options (checkboxes):**
- [ ] Include timestamps (default: OFF)
- [ ] Include system messages (default: OFF) - join/leave/topic changes

### Output
- Formatted Markdown in readonly display area
- "Copy to Clipboard" button with visual feedback ("Copied!")
- Show character/word count (helpful for AI context limits)

## Output Format

```markdown
@alice: Hey team, can we discuss the API changes?

@bob: Sure, I've been looking at the auth flow. **Important**: we need to handle token refresh.

@alice: Good point. Let's sync with @charlie on this.
[thread: 5 replies]

@bob: Here's the code I'm thinking:
```python
def refresh_token(token):
    return new_token
```

@alice: Looks good! #backend team should review.
```

### With timestamps enabled:
```markdown
[10:23] @alice: Hey team, can we discuss the API changes?

[10:25] @bob: Sure, I've been looking at the auth flow.
```

## UI/UX Design

### Layout
```
┌─────────────────────────────────────────────────┐
│  Slack Text Cleaner                             │
│  Clean up copy/pasted Slack conversations       │
├─────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────┐    │
│  │ Paste Slack conversation here...        │    │
│  │                                         │    │
│  │                                         │    │
│  └─────────────────────────────────────────┘    │
│                                                 │
│  Options:                                       │
│  [ ] Include timestamps                         │
│  [ ] Include system messages (joins, etc.)      │
│                                                 │
│  ┌─────────────────────────────────────────┐    │
│  │ Cleaned Markdown output appears here... │    │
│  │                                         │    │
│  │                                         │    │
│  └─────────────────────────────────────────┘    │
│                                                 │
│  [Copy to Clipboard]        142 words, 823 chars│
│                                                 │
│  ← Back to tools                                │
└─────────────────────────────────────────────────┘
```

### Behavior
- Output updates in real-time as user pastes/edits input
- Options checkboxes trigger immediate re-processing
- Copy button shows "Copied!" feedback for 2 seconds
- Empty input shows helpful placeholder in output area

## Edge Cases & Error Handling

| Scenario | Behavior |
|----------|----------|
| Empty input | Show placeholder: "Cleaned output will appear here" |
| No recognizable Slack format | Pass through as-is (best effort) |
| Only system messages (with option OFF) | Show message: "No content after filtering" |
| Very long conversations | No limit, but show word/char count for awareness |
| Malformed timestamps | Skip timestamp, keep message content |
| Custom Slack emojis (`:custom_emoji:`) | Treat as inline emoji, keep them |
| Unicode emojis in reactions | Remove with count (e.g., `😀 3`) |

## Technical Implementation Notes

### Parsing Strategy

Slack copy/paste format typically looks like:
```
Username
10:23 AM

Message content here
:+1: 3  :heart: 2

Another Username
10:25 AM

Their message
5 replies
```

**Regex patterns needed:**
1. Username detection: Line containing only letters, numbers, spaces, hyphens, apostrophes
2. Timestamp: `\d{1,2}:\d{2}\s*(AM|PM)?` on its own line
3. Reactions: `(:\w+:|[\u{1F300}-\u{1F9FF}])\s*\d+` pattern
4. Thread indicator: `\d+\s+repl(y|ies)`
5. System messages: "joined #channel", "set the channel topic", "left the channel"

### Formatting Conversion
- Must handle nested formatting carefully
- Code blocks should be detected first and excluded from other transformations
- Links with display text: `<url|display>` → `[display](url)`

## Testing Checklist

- [ ] Basic conversation with 2-3 users converts correctly
- [ ] Emoji reactions are stripped
- [ ] Inline emojis (in message text) are preserved
- [ ] *bold* converts to **bold**
- [ ] ~strike~ converts to ~~strike~~
- [ ] Code blocks preserved exactly
- [ ] Links remain clickable/valid
- [ ] Timestamps toggle works
- [ ] System messages toggle works
- [ ] Thread indicators show correctly
- [ ] Copy button works with feedback
- [ ] Mobile responsive layout
- [ ] No console errors

## Prior Art

- [Slack Copy Paste by Daniel Na](https://www.danielna.com/labs/slack-copy-paste/) - Similar tool, simpler output format
- Common pain point discussed on [GitLab](https://gitlab.com/gitlab-org/gitlab/-/issues/28755) and [Quora](https://www.quora.com/What-is-the-best-way-to-copy-paste-Slack-chat-to-other-place-e-g-JIRA-ticket-to-retain-most-data-formatting-images)

## File Locations

- New file: `slack-text-cleaner.html`
- Update: `index.html` (add to tools list)
- Update: `colophon.html` (add to tools list)

## Open Questions

None - ready for implementation.
