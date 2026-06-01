---
source_type: 'developers'
source_area: 'codex_sdk'
source_url: 'https://developers.openai.com/codex/sdk'
source_last_modified: '2026-04-25T06:33:55Z'
source_etag: 'W/"28bd573a593b19ab68c959d1ee4f6338"'
codex_cli_versions: ["0.125.0", "0.128.0", "0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0", "0.134.0", "0.135.0", "0.136.0"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0", "codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0", "codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0"]
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

The Python SDK is experimental and controls the local Codex app-server over JSON-RPC. It requires Python 3.10 or later and a local checkout of the open-source Codex repo.

### Installation

From the Codex repo root, install the SDK in editable mode:

```
cd sdk/python
python -m pip install -e .
```

For manual local SDK usage, pass `AppServerConfig(codex_bin=...)` to point at a local `codex` binary, or use the repo examples and notebook bootstrap.

### Usage

Start Codex, create a thread, and run a prompt:

```
from codex_app_server import Codex

with Codex() as codex:
    thread = codex.thread_start(model="gpt-5.4")
    result = thread.run("Make a plan to diagnose and fix the CI failures")
    print(result.final_response)
```

Use `AsyncCodex` when your application is already asynchronous:

```
import asyncio

from codex_app_server import AsyncCodex

async def main() -> None:
    async with AsyncCodex() as codex:
        thread = await codex.thread_start(model="gpt-5.4")
        result = await thread.run("Implement the plan")
        print(result.final_response)

asyncio.run(main())
```

For more details, check out the [Python repo](https://github.com/openai/codex/tree/main/sdk/python).

