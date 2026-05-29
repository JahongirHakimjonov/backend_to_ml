---
description: Build all 3 languages and serve via http.server on port 3000
allowed-tools: Bash, Agent
---

# 3-language preview

Steps:
1. Delegate to the `mdbook-builder` subagent and run the full 3-language pipeline (uz default + ru + en + fix-canonical-urls + sitemap).
2. After the build succeeds, run `cd book && python3 -m http.server 3000` in the background.
3. Summarize URLs for the user:
   - `http://localhost:3000/` (Uzbek)
   - `http://localhost:3000/ru/` (Russian)
   - `http://localhost:3000/en/` (English)
4. Remind them that there is no hot reload — rebuild on every change.

To stop the server: `lsof -i :3000` to find the PID, then `kill`.
