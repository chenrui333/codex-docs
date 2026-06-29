---
source_type: 'developers'
source_area: 'codex_sdk'
source_url: 'https://developers.openai.com/codex/sdk'
source_last_modified: '2026-06-09T17:53:49Z'
source_etag: 'W/"a71cb851c75c9d6dbd5156a85704ff46"'
codex_cli_versions: ["0.125.0", "0.128.0", "0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0", "0.134.0", "0.135.0", "0.136.0", "0.137.0", "0.138.0", "0.139.0", "0.140.0", "0.141.0", "0.142.0", "0.142.1", "0.142.2", "0.142.3", "0.142.4"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0", "codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0", "codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0", "codex-cli 0.137.0", "codex-cli 0.138.0", "codex-cli 0.139.0", "codex-cli 0.140.0", "codex-cli 0.141.0", "codex-cli 0.142.0", "codex-cli 0.142.1", "codex-cli 0.142.2", "codex-cli 0.142.3", "codex-cli 0.142.4"]
---

# SDK – Codex | OpenAI Developers

Source: https://developers.openai.com/codex/sdk

If you use Codex through the Codex CLI, the IDE extension, or Codex Web, you can also control it programmatically.

Use the SDK when you need to:

- Control Codex as part of your CI/CD pipeline
- Create your own agent that can engage with Codex to perform complex engineering tasks
- Build Codex into your own internal tools and workflows
- Integrate Codex within your own application

## TypeScript library

The TypeScript library provides a way to control Codex from within your application that’s more comprehensive and flexible than non-interactive mode.

Use the library server-side; it requires Node.js 18 or later.

### Installation

To get started, install the Codex SDK using `npm`:

```
npm install @openai/codex-sdk
```

### Usage

Start a thread with Codex and run it with your prompt.

```
import { Codex } from "@openai/codex-sdk";

const codex = new Codex();
const thread = codex.startThread();
const result = await thread.run(
  "Make a plan to diagnose and fix the CI failures"
);

console.log(result);
```

Call `run()` again to continue on the same thread, or resume a past thread by providing a thread ID.

```
// running the same thread
const result = await thread.run("Implement the plan");

console.log(result);

// resuming past thread

const threadId = "<thread-id>";
const thread2 = codex.resumeThread(threadId);
const result2 = await thread2.run("Pick up where you left off");

console.log(result2);
```

For more details, check out the [TypeScript repo](https://github.com/openai/codex/tree/main/sdk/typescript).

## Python library

The Python SDK controls the local Codex app-server over JSON-RPC. It requires Python 3.10 or later. Published SDK builds include a pinned Codex CLI runtime dependency.

### Installation

To install the SDK run:

```
pip install openai-codex
```

Published SDK builds automatically use their pinned runtime. Pass `CodexConfig(codex_bin=...)` only when you intentionally want to run against a specific local Codex executable.

While the Python SDK is in beta, `pip install openai-codex` selects the latest
published beta build. After a stable SDK release exists, use
`pip install --pre openai-codex` to opt in to newer prerelease builds.

### Usage

Start Codex, create a thread, and run a prompt:

```
from openai_codex import Codex, Sandbox

with Codex() as codex:
    thread = codex.thread_start(
        model="gpt-5.4",
        sandbox=Sandbox.workspace_write,
    )
    result = thread.run("Make a plan to diagnose and fix the CI failures")
    print(result.final_response)
```

Use `AsyncCodex` when your application is already asynchronous:

```
import asyncio

from openai_codex import AsyncCodex

async def main() -> None:
    async with AsyncCodex() as codex:
        thread = await codex.thread_start(model="gpt-5.4")
        result = await thread.run("Implement the plan")
        print(result.final_response)

asyncio.run(main())
```

### Sandbox presets

Use the same `Sandbox` presets when creating a thread or changing its filesystem
access for a later turn:

```
from openai_codex import Codex, Sandbox

with Codex() as codex:
    thread = codex.thread_start(sandbox=Sandbox.workspace_write)
    thread.run("Make the requested change.")
    review = thread.run("Review the diff only.", sandbox=Sandbox.read_only)
```

Available presets:

- `Sandbox.read_only`: Read files without allowing writes.
- `Sandbox.workspace_write`: Read files and write inside the workspace and configured writable roots.
- `Sandbox.full_access`: Run without filesystem access restrictions.

When you omit `sandbox=`, app-server uses its configured default. A sandbox
passed to `run(...)` or `turn(...)` applies to that turn and later turns
on the thread.

For more details, check out the [Python repo](https://github.com/openai/codex/tree/main/sdk/python).

