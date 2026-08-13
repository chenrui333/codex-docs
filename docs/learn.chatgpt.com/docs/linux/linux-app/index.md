---
source_type: 'learn'
source_area: 'learn_linux'
source_url: 'https://learn.chatgpt.com/docs/linux/linux-app'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.147.0"]
codex_cli_versions_raw: ["codex-cli 0.147.0"]
---

# ChatGPT desktop app for Linux

Source: https://learn.chatgpt.com/docs/linux/linux-app

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

The ChatGPT desktop app for Linux is available in preview. Install the package
for your Linux distribution and processor architecture, then sign in with your
ChatGPT account to work with projects, local files, and Codex.

## Supported distributions and architectures

The preview supports the desktop versions of these Linux distributions:

- Ubuntu 24.04 LTS and 26.04 LTS
- Debian 13
- Fedora 43 and 44

Each supported distribution has packages for x64 and ARM64 processors. To check
your processor architecture, run:

```bash
uname -m
```

The output `x86_64` identifies an x64 processor. The output `aarch64` or
`arm64` identifies an ARM64 processor.

## Download the right package

Choose `.deb` for Ubuntu or Debian, and `.rpm` for Fedora:

| Distribution     | Architecture | Download                                                                                                          |
| ---------------- | ------------ | ----------------------------------------------------------------------------------------------------------------- |
| Ubuntu or Debian | x64          | [Download `.deb` for x64](https://persistent.oaistatic.com/codex-app-prod/linux/deb/latest/chatgpt_amd64.deb)     |
| Ubuntu or Debian | ARM64        | [Download `.deb` for ARM64](https://persistent.oaistatic.com/codex-app-prod/linux/deb/latest/chatgpt_arm64.deb)   |
| Fedora           | x64          | [Download `.rpm` for x64](https://persistent.oaistatic.com/codex-app-prod/linux/rpm/latest/chatgpt.x86_64.rpm)    |
| Fedora           | ARM64        | [Download `.rpm` for ARM64](https://persistent.oaistatic.com/codex-app-prod/linux/rpm/latest/chatgpt.aarch64.rpm) |

## Install on Ubuntu or Debian

Download the `.deb` package for your processor architecture. Then open a
terminal, change to the directory containing the package, and install it with
`apt`:

```bash
cd ~/Downloads
sudo apt install ./chatgpt_amd64.deb
```

For ARM64, replace `chatgpt_amd64.deb` with `chatgpt_arm64.deb`.

Open **ChatGPT** from your applications menu, or run `chatgpt` in a terminal.
Sign in with your ChatGPT account and follow the
[desktop app quickstart](https://learn.chatgpt.com/docs/quickstart?setup=app).

## Install on Fedora

Download the `.rpm` package for your processor architecture. Then open a
terminal, change to the directory containing the package, and install it with
`dnf`:

```bash
cd ~/Downloads
sudo dnf install ./chatgpt.x86_64.rpm
```

For ARM64, replace `chatgpt.x86_64.rpm` with `chatgpt.aarch64.rpm`.

Open **ChatGPT** from your applications menu, or run `chatgpt` in a terminal.
Sign in with your ChatGPT account and follow the
[desktop app quickstart](https://learn.chatgpt.com/docs/quickstart?setup=app).

## Update the app

The package configures the signed OpenAI package repository during installation.
Use your distribution's package manager to install later updates.

On Ubuntu or Debian, run:

```bash
sudo apt update
sudo apt install --only-upgrade chatgpt
```

On Fedora, run:

```bash
sudo dnf upgrade --refresh chatgpt
```

## Compatibility and limitations

The preview supports the desktop distributions listed in
[Supported distributions and architectures](#supported-distributions-and-architectures).
Other Linux distributions may work but aren't formally supported.

Some features have separate platform requirements. For example,
[Computer Use](https://learn.chatgpt.com/docs/computer-use) is available on macOS and Windows but not
yet in the Linux preview. A future release will add Linux support.

## Wayland support

Native Wayland support is experimental and will continue to improve. In a Wayland
session, the app uses XWayland when available. To explicitly select native
Wayland, fully quit the app and launch it from a terminal:

```bash
chatgpt --ozone-platform=wayland
```

Some features, such as floating windows, window positioning, focus, and keyboard
shortcuts, may not fully work while native Wayland support matures.

## Next steps

- Follow the [desktop app quickstart](https://learn.chatgpt.com/docs/quickstart?setup=app).
- Set up the [Chrome extension](https://learn.chatgpt.com/docs/chrome-extension) for browser integration.
- Review [permissions](https://learn.chatgpt.com/docs/permissions) for local projects and commands.
