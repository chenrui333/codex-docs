---
source_type: 'learn'
source_area: 'learn_dots'
source_url: 'https://learn.chatgpt.com/docs/dots/controls'
source_kind: 'learn_markdown'
---

# Control your dot

Source: https://learn.chatgpt.com/docs/dots/controls

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Built-in safeguards, existing app permissions, and automatic approval checks
apply from the start. You can review ongoing work, add instructions, or set
optional custom rules.

## Review work

In the desktop app, open your dot's profile and select **Activity**. Select a
task to review its progress, files, and results, including work happening in the
background. If it's waiting for a decision, app connection, sign-in, or approval,
open the request and respond to continue. You can change direction as work
continues.

Open **Scheduled** to review your dot's scheduled tasks. Check the task's
instructions, timing, and destination. See
[tasks and memory](https://learn.chatgpt.com/docs/dots/tasks-and-memory) for recurring work.

## How action review works

Before your dot takes an action that could affect your accounts or share
information, an automatic review checks it against your instructions,
permissions, custom rules, and built-in safety requirements. The review
determines whether the action can proceed, needs your approval, or includes a
step you must do yourself. For example, you must change a password yourself.

Give ongoing instructions a clear scope: who can take part, what should happen,
and when. Asking your dot to draft replies doesn't give it permission to send
them. A specific instruction can cover future actions within that scope; an
action outside it needs another decision.

Your dot can also research information from apps you've connected to look for
ways to help. The tools it uses for that research can't send messages, change
app content, or control your browser or computer. Any follow-up action is
subject to the same permissions and safety requirements.

## Set custom rules

Custom rules are optional controls for specific ongoing boundaries. Start with
clear instructions in your conversation; you don’t need to create a rule for
every approval.

After setting up your dot, open **Settings** > **Personalization** and select
**Custom rules** under **Permissions**.

Select **Add**, describe the action, choose how your dot should handle it,
and select **Add rule**. The choices are:

| Rule                        | Intended behavior                                                                        |
| --------------------------- | ---------------------------------------------------------------------------------------- |
| Take action without asking  | Take the specified action without asking for approval.                                   |
| Take action when you say so | Proceed when you explicitly request the action; otherwise ask immediately before acting. |
| Ask before taking action    | Ask for approval before taking the specified action.                                     |
| Hand off to you             | Ask you to take the action instead.                                                      |

For example, you could choose **Ask before taking action** for sending messages
to customers, or **Hand off to you** for deleting shared project files. Use your
conversation for preferences such as writing style or how you like updates;
custom rules control when your dot can take an action.

Saved custom rules apply to your dot in the same account. They can give your
dot permission for particular actions, require it to check with you, or prevent
it from taking an action. They are instructions your dot tries to follow, and
it can make mistakes. They don't grant access to an app or computer, override
built-in safety requirements, or remove required confirmations such as approval
to use a saved login.

Use a rule's menu to edit or delete it. Select **Open Plugins** to review
**Plugin permissions**, which control app actions separately from custom rules.
If your workspace disables custom rules, you can't edit saved rules, and they
don't apply. See [Configure dots permissions](#for-workspace-admins).

<a id="for-workspace-admins"></a>

**For workspace admins:** See [Set up dots for work](https://learn.chatgpt.com/docs/enterprise/dots-admin-guide) for workspace permissions, setup, and security and governance guidance.

## Manage data settings

Your ChatGPT data controls also apply to eligible conversations with your dot
and the work it carries out. OpenAI doesn't train models directly on proactive
research or its private notes. If information from that research becomes part
of an eligible conversation or task, your data settings apply. See [data controls in ChatGPT](https://help.openai.com/en/articles/7730893-data-controls-in-chatgpt).

## Stop work

Pausing your dot, stopping a delegated task, and canceling a schedule have
different effects:

- **Pause** stops your dot's current main task. It doesn't stop every delegated
  task or cancel future scheduled runs.
- Open a delegated task in **Activity** to inspect and stop that task.
- Open **Scheduled** to disable or delete the recurring task you want to end.

Use **Resume** to continue a paused dot. Stopping work doesn't undo completed
actions. Review active tasks and schedules separately.

<a id="reset-your-dot"></a>

## Delete your dot

Use **Delete** to delete your dot. Read the confirmation for how deletion handles conversations, memories, and scheduled tasks. Save any results you need before confirming; the action cannot be undone.

Deleting your dot doesn’t undo changes already made in connected apps or recall messages already delivered to other people.
