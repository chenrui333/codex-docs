---
source_type: 'platform_tool_guide'
source_url: 'https://developers.openai.com/api/docs/guides/tools-apply-patch'
source_last_modified: '2026-04-25T10:17:19Z'
source_etag: 'W/"dd05d3c7ce6f524e30a889027f7bd3c1"'
codex_cli_versions: ["0.125.0"]
codex_cli_versions_raw: ["codex-cli 0.125.0"]
---

# Apply Patch

Source: https://developers.openai.com/api/docs/guides/tools-apply-patch

The `apply_patch` tool lets GPT-5.1 create, update, and delete files in your codebase using structured diffs. Instead of just suggesting edits, the model emits patch operations that your application applies and then reports back on, enabling iterative, multi-step code editing workflows.

## When to use

Some common scenarios where you would use apply_patch:

- **Multi-file refactors** – Rename symbols, extract helpers, or reorganize modules across many files at once.
- **Bug fixes** – Have the model both diagnose issues and emit precise patches.
- **Tests & docs generation** – Create new test files, fixtures, and documentation alongside code changes.
- **Migrations & mechanical edits** – Apply repetitive, structured updates (API migrations, type annotations, formatting fixes, etc.).

If you can describe your repo and desired change in text, apply_patch can usually generate the corresponding diffs.

## Use apply patch tool with Responses API

At a high level, using `apply_patch` with the Responses API looks like this:

1. **Call the Responses API with the `apply_patch` tool**
   - Provide the model with context about available files (or a summary) in your `input`, or give the model tools for exploring your file system.
   - Enable the tool with `tools=[{"type": "apply_patch"}]`.
2. **Let the model return one or more patch operations**
   - The Response output includes one or more `apply_patch_call` objects.
   - Each call describes a single file operation: create, update, or delete.
3. **Apply patches in your environment**
   - Run a patch harness or script that:
     - Interprets the `operation` diff for each `apply_patch_call`.
     - Applies the patch to your working directory or repo.
     - Records whether each patch succeeded and any logs or error messages.
4. **Report patch results back to the model**
   - Call the Responses API again, either with `previous_response_id` or by passing back your conversation items into `input`.
   - Include an `apply_patch_call_output` event for each `call_id`, with a `status` and optional `output` string.
   - Keep `tools=[{"type": "apply_patch"}]` so the model can continue editing if needed.
5. **Let the model continue or explain changes**
   - The model may issue more `apply_patch_call` operations, or
   - Provide a human-facing explanation of what it changed and why.

## Example: Renaming a function with Apply Patch Tool

**Step 1: Ask the model to plan and emit patches**

**Example `apply_patch_call` object**

**Step 2: Apply the patch and send results back**

If a patch fails (for example, file not found), set `status: "failed"` and include a helpful `output` string so the model can recover:

## Apply patch operations

| Operation Type | Purpose                            | Payload                                                          |
| -------------- | ---------------------------------- | ---------------------------------------------------------------- |
| `create_file`  | Create a new file at `path`.       | `diff` is a V4A diff representing the full file contents.        |
| `update_file`  | Modify an existing file at `path`. | `diff` is a V4A diff with additions, deletions, or replacements. |
| `delete_file`  | Remove a file at `path`.           | No `diff`; delete the file entirely.                             |

Your patch harness is responsible for interpreting the V4A diff format and applying changes. For reference implementations, see the [Python Agents SDK](https://github.com/openai/openai-agents-python/blob/main/src/agents/apply_diff.py) or [TypeScript Agents SDK](https://github.com/openai/openai-agents-js/blob/main/packages/agents-core/src/utils/applyDiff.ts) code.

## Implementing the patch harness

When using the `apply_patch` tool, you don’t provide an input schema; the model knows how to construct `operation` objects. Your job is to:

1. **Parse operations from the Response**
   - Scan the Response for items with `type: "apply_patch_call"`.
   - For each call, inspect `operation.type`, `operation.path`, and any potential `diff`.
2. **Apply file operations**
   - For `create_file` and `update_file`, apply the V4A diff to the file system or in-memory workspace.
   - For `delete_file`, remove the file at `path`.
   - Record whether each operation succeeded and any logs or error messages.
3. **Return `apply_patch_call_output` events**
   - For each `call_id`, emit exactly one `apply_patch_call_output` event with:
     - `status: "completed"` if the operation was applied successfully.
     - `status: "failed"` if you encountered an error (include a short human-readable `output` string).

### Safety and robustness

- **Path validation**: Prevent directory traversal and restrict edits to allowed directories.
- **Backups**: Consider backing up files (or working in a scratch copy) before applying patches.
- **Error handling**: Always return a `failed` status with an informative `output` string when patches cannot be applied.
- **Atomicity**: Decide whether you want “all-or-nothing” semantics (rollback if any patch fails) or per-file success/failure.

## Use the apply patch tool with the Agents SDK

Alternatively, you can use the [Agents SDK](https://developers.openai.com/api/docs/guides/tools#usage-in-the-agents-sdk) to use the apply patch tool. You'll still have to implement the harness that handles the actual file operations but you can use the `applyDiff` function to handle the diff processing.

You can find full working examples on GitHub.

<a
  href="https://github.com/openai/openai-agents-js/blob/main/examples/tools/applyPatch.ts"
  target="_blank"
  rel="noreferrer"
>

<span slot="icon">
      </span>
    Example of how to use the apply patch tool with the Agents SDK in TypeScript

</a>

<a
  href="https://github.com/openai/openai-agents-python/blob/main/examples/tools/apply_patch.py"
  target="_blank"
  rel="noreferrer"
>

<span slot="icon">
      </span>
    Example of how to use the apply patch tool with the Agents SDK in Python

</a>

## Handling common errors

Use `status: "failed"` plus a clear `output` message to help the model recover.

<div data-content-switcher-pane data-value="file-missing">
    <div class="hidden">File not found</div>
    </div>
  <div data-content-switcher-pane data-value="patch-conflict" hidden>
    <div class="hidden">Patch conflict</div>
    </div>

The model can then adjust future diffs (for example, by re-reading a file in your prompt or simplifying a change) based on these error messages.

## Best practices

- **Give clear file context**
  - When you call the Responses API, include either an inline snapshot of your files (as in the example), or give the model tools for exploring your filesystem (like the `shell` tool).
- **Consider using with the `shell` tool**
  - When used in conjunction with the `shell` tool, the model can explore file system directories, read files, and grep for keywords, enabling agentic file discovery and editing.
- **Encourage small, focused diffs**
  - In your system instructions, nudge the model toward minimal, targeted edits rather than huge rewrites.
- **Make sure changes apply cleanly**
  - After a series of patches, run your tests or linters and share failures back in the next `input` so the model can fix them.

## Usage notes

<table>
<tbody>

<tr>
  <th>API Availability</th>
  <th>Supported models</th>
</tr>

<tr>
  <td>
    <div className="mb-1 flex items-center gap-2">
      [Responses](https://developers.openai.com/api/docs/api-reference/responses)
    </div>
    <div className="mb-1 flex items-center gap-2">
      [Chat Completions](https://developers.openai.com/api/docs/api-reference/chat)
    </div>
    <div className="mb-1 flex items-center gap-2">
      [Assistants](https://developers.openai.com/api/docs/api-reference/assistants)
    </div>
  </td>
  <td style={{ maxWidth: "150px" }}>
    [GPT-5.5](https://developers.openai.com/api/docs/models/gpt-5.5)
    <br />
    [GPT-5.4](https://developers.openai.com/api/docs/models/gpt-5.4)
    <br />
    [GPT-5.2](https://developers.openai.com/api/docs/models/gpt-5.2)
    <br />
    [GPT-5.1](https://developers.openai.com/api/docs/models/gpt-5.1)
  </td>
</tr>

</tbody>
</table>
