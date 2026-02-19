# Review

Source: https://developers.openai.com/codex/app/review

Review and iterate with Codex on changes inside the app

The review pane helps you understand what Codex changed, give targeted feedback, and decide what to keep.

It only works for projects that live inside a Git repository. If your project
isn’t a Git repository yet, the review pane will prompt you to create one.

## What changes it shows

The review pane reflects the state of your Git repository, not just what Codex
edited. That means it will show:

- Changes made by Codex
- Changes you made yourself
- Any other uncommitted changes in the repo

By default, the review pane focuses on **uncommitted changes**. You can also
switch the scope to:

- **All branch changes** (diff against your base branch)
- **Last turn changes** (just the most recent assistant turn)

When working locally, you can also toggle between **Unstaged** and **Staged**
changes.

## Navigating the review pane

- Clicking a file name typically opens that file in your chosen editor. You can choose the default editor in [settings](/codex/app/settings).
- Clicking the file name background expands or collapses the diff.
- Clicking a single line while holding `Cmd` pressed will open the line in your chosen editor.
- If you are happy with a change you can [stage the changes or revert changes](#staging-and-reverting-files) you don’t like.

## Inline comments for feedback

Inline comments let you attach feedback directly to specific lines in the diff.
This is often the fastest way to guide Codex to the right fix.

To leave an inline comment:

1. Open the review pane.
2. Hover the line you want to comment on.
3. Click the **+** button that appears.
4. Write your feedback and submit it.
5. Once you are done with all your feedback, send a message back to the thread.

Because the comment is anchored to a line, Codex can usually respond more
precisely than with a general instruction.

Inline comments are treated as review guidance. After leaving comments, send a
follow-up message that makes your intent explicit, for example “Address the
inline comments and keep the scope minimal.”

## Code review results

If you use `/review` to run a code review, comments will show up directly
inline in the review pane.

![Inline code review comments displayed in the review pane](/images/codex/app/inline-code-review-light.webp) ![Inline code review comments displayed in the review pane](/images/codex/app/inline-code-review-dark.webp)

![Inline code review comments displayed in the review pane](/images/codex/app/inline-code-review-light.webp) ![Inline code review comments displayed in the review pane](/images/codex/app/inline-code-review-dark.webp)

## Staging and reverting files

The review pane includes Git actions so you can shape the diff before you
commit.

You can stage, unstage, or revert changes at multiple levels:

- **Entire diff**: use the action buttons in the review header (for example,
  “Stage all” or “Revert all”)
- **Per file**: stage, unstage, or revert an individual file
- **Per hunk**: stage, unstage, or revert a single hunk

Use staging when you want to accept part of the work, and revert when you want
to discard it.

### Partially staged states

Git can represent both staged and unstaged changes in the same file. When that
happens, it can look like the pane is showing “the same file twice” across
staged and unstaged views. That’s normal Git behavior.

[Previous

Settings](/codex/app/settings)[Next

Automations](/codex/app/automations)

