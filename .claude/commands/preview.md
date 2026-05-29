---
description: Serve the Uzbek mdBook with live reload
allowed-tools: Bash
---

# mdBook preview (uz)

Run `mdbook serve --open`. This serves the default (Uzbek) variant with live reload in the browser.

Note: `mdbook serve` only serves the default language — `/ru/` and `/en/` return 404. For all three languages, use `/preview-all`.

If `mdbook` is not found, remind the user to run `export PATH="$HOME/.cargo/bin:$PATH"`.

The command runs in the foreground — Ctrl+C to stop the server.
