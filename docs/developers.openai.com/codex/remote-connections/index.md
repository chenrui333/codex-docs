---
source_type: 'developers'
source_area: 'codex_cli_docs'
source_url: 'https://developers.openai.com/codex/remote-connections'
source_last_modified: '2026-05-18T21:46:01Z'
source_etag: 'W/"5e4213f87e766fc56fb214a79314a19f"'
codex_cli_versions: ["0.125.0", "0.128.0", "0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0", "codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0"]
---

# Remote connections – Codex | OpenAI Developers

Source: https://developers.openai.com/codex/remote-connections

Remote connections let you use Codex from another device or another machine.
Use Codex in the ChatGPT mobile app to work with Codex on a connected Mac,
continue work from another Codex App device, or connect the Codex App to
projects on an SSH host.

Remote access uses the connected host’s projects, threads, files, credentials,
permissions, plugins, Computer Use, browser setup, and local tools.

## What you can do remotely

- Start new threads in projects on the host, or continue existing ones.
- Send follow-up instructions, answer questions, and steer active work.
- Approve commands and other actions.
- Review outputs, diffs, test results, terminal output, and screenshots.
- Get notified when Codex completes a task or needs your attention.
- Switch between connected hosts and threads.

The next sections cover using Codex in the ChatGPT mobile app to control a Codex
App host. To connect Codex to a project on an SSH host, see
[connect to an SSH host](#connect-to-an-ssh-host).

![Codex mobile setup screen alongside the ChatGPT mobile Codex project list](/images/codex/app/mobile-setup-light.webp)

## Before you set up mobile access

Make sure you have:

- Codex access in the ChatGPT account and workspace you want to use.
- The latest ChatGPT mobile app on an iOS or Android device. If you do not see
  Codex in the ChatGPT mobile app, update ChatGPT first.
- The latest Codex App for macOS running on a Mac host that is awake, online,
  and signed in to the same account and workspace. Mobile setup starts from the
  Codex App; you cannot set it up from the Codex CLI or IDE Extension.
- Any required multi-factor authentication, SSO, or passkey configuration for
  that account or workspace.

If you use Codex through a ChatGPT workspace, your admin may need to enable
Remote Control access before you can connect from your phone.

## Set up mobile access

Start in the Codex App on the host you want to connect. The setup flow enables
remote access for that host, then shows a QR code you can scan from your phone.

1. Start Codex mobile setup.

   Open Codex on the host and select **Set up Codex mobile** in the
   sidebar.
2. Scan the QR code.

   Use your phone to scan the QR code shown by Codex. The code opens ChatGPT so
   you can finish connecting the mobile app to the host.
3. Finish setup in ChatGPT.

   ChatGPT opens the Codex mobile setup flow. Confirm the same ChatGPT account
   and workspace, then complete any required multi-factor authentication, SSO,
   or passkey steps. After setup succeeds, the host appears in Codex on your
   phone.
4. Review host settings.

   In Codex on the host, use **Settings > Connections** to manage connected
   devices. You can also choose whether to keep the computer awake, enable
   Computer Use, or install the Chrome extension.

![Connections settings showing devices that can control this Mac and remote access settings](/images/codex/app/mobile-control-this-mac-framed-light.webp)

## Choose what to connect

Start with the Mac laptop or desktop where you already use Codex. Add an
always-on Mac or SSH host when you need continuous access or a different
environment.

### Your Mac laptop or desktop

Connect the Mac where you already run Codex day to day. This gives remote access
to the same projects, threads, credentials, plugins, and local setup you already
use.

If that Mac sleeps, loses network access, or closes Codex, remote access stops
until it is available again. If you use this computer as your host device, keep
it plugged in and turn on **Keep this Mac awake** in the host’s connection
settings.

On a Mac laptop, remote access can stay available with the lid open while the
computer is plugged in. With the lid closed, connect an external display as
well. Choosing **Sleep** still stops remote access.

### A dedicated always-on Mac

Use a dedicated always-on Mac when you want Codex to stay reachable for
longer-running work.

Install the projects, credentials, plugins, MCP servers, and tools Codex should
use on that machine.

### A remote development environment

Use an SSH host or managed devbox when the project already lives in a remote
environment. Connect the Codex App host to that environment first; your phone
still connects to the Codex App host, and Codex works in the remote environment
with its dependencies, security policies, and compute resources.

For SSH setup details, see [connect to an SSH host](#connect-to-an-ssh-host).

For browser or desktop tasks on an always-on Mac or remote host, enable
Computer Use and install the Chrome extension on that host.

## What comes from the connected host

Your phone sends prompts, approvals, and follow-up messages to Codex. The
connected host provides the environment Codex uses.

That means:

- Repository files and local documents come from the connected host.
- Shell commands run on that host or remote environment.
- Any plugin installed on that host is available when you use Codex remotely.
- MCP servers, skills, browser access, and Computer Use come from that host’s
  configuration.
- Signed-in websites and desktop apps are available only when the host can
  access them.
- Sandboxing, security controls, and action approvals still apply to the
  connected session.

Codex uses a secure relay layer to keep trusted machines reachable across your
authorized ChatGPT devices without exposing them directly to the public
internet.

## Pick up work from another device

You can continue work from another signed-in Codex App device. For example, if
your laptop is unavailable, you can start a thread from your phone on an
always-on host, then later open Codex on your laptop and continue that same
thread there.

In Codex on the laptop, use **Settings > Connections > Control other devices**
to add the other host. A device can allow remote access and control another
device at the same time.

![Connections settings showing another device available under Control other devices](/images/codex/app/mobile-control-other-devices-framed-light.webp)

## Connect to an SSH host

In the Codex App, add remote projects from an SSH host and run threads against
the remote filesystem and shell. Remote project threads run commands, read
files, and write changes on the remote host.

Keep the remote host configured with the same security expectations you use for
normal SSH access: trusted keys, least-privilege accounts, and no
unauthenticated public listeners.

1. Add the host to your SSH config so Codex can auto-discover it.

   ```
   Host devbox
     HostName devbox.example.com
     User you
     IdentityFile ~/.ssh/id_ed25519
   ```

   Codex reads concrete host aliases from `~/.ssh/config`, resolves them with
   OpenSSH, and ignores pattern-only hosts.
2. Confirm you can SSH to the host from the machine running the Codex App.

   ```
   ssh devbox
   ```
3. Install and authenticate Codex on the remote host.

   The app starts the remote Codex app server through SSH, using the remote
   user’s login shell. Make sure the `codex` command is available on the
   remote host’s `PATH` in that shell.
4. In the Codex App, open **Settings > Connections**, add or enable the SSH
   host, then choose a remote project folder.

![Codex app settings showing SSH remote connections](/images/codex/app/remote-connections-light.webp)

## Authentication and network exposure

Remote connections use SSH to start and manage the remote Codex app server.
Don’t expose app-server transports directly on a shared or public network.

If you need to reach a remote machine outside your current network, use a VPN
or mesh networking tool instead of exposing the app server directly to the
internet.

## Troubleshooting

### You do not see the host on your phone

Confirm that the Codex App is running on the host, **Allow other devices to
connect** is enabled, and the same ChatGPT account and workspace are selected on
both devices.

### The approval request does not appear

Open Codex in the ChatGPT mobile app. Confirm that the phone and host use the
same ChatGPT account and workspace, then scan the QR code again or restart setup
from the host. If you use a ChatGPT workspace, ask your admin to confirm that
Remote Control access is enabled.

### The remote session disconnects

Check whether the host went to sleep, lost network access, or closed Codex.
Keep the host awake and connected while Codex works.

### Authentication blocks setup

Complete the account or workspace authentication prompt shown during setup. If
your organization requires SSO, multi-factor authentication, or a passkey,
finish that flow before trying again. If setup still fails, ask your workspace
admin to confirm that Remote Control access is enabled.

## See also

- [Codex App](/codex/app)
- [Codex App features](/codex/app/features)
- [Codex App settings](/codex/app/settings)
- [Computer Use](/codex/app/computer-use)
- [Chrome extension](/codex/app/chrome-extension)
- [Command line options](/codex/cli/reference)
- [Authentication](/codex/auth)

