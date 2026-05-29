# Security Policy

Thank you for helping keep this project secure! The guidelines below explain how to report vulnerabilities responsibly.

---

## Supported versions

The project is currently in active development. Security updates are provided for the following versions:

| Version | Supported |
|---------|-----------|
| `main` (active branch) | Yes |
| `v1.x` (future) | Yes (after release) |
| Old tags / forks | No |

> Note: This is a book project (mdBook), so most "security" concerns here are **bugs in code examples**, **CVEs in dependencies**, or **broken external links**. Classic web/backend vulnerabilities are largely not applicable.

---

## How to report a vulnerability

### What NOT to do

- **Do NOT open a public GitHub issue** — public disclosure can cause harm.
- Do not discuss the issue in **public Telegram groups**.
- Do not **share the vulnerability** with others until a fix is released.

### What to do

Report the vulnerability privately through one of the channels below:

| Channel | Contact | Recommended for |
|---------|---------|-----------------|
| Email | jahongirhakimjonov@gmail.com | Primary channel for all reports |
| Telegram | [@ja_khan_gir](https://t.me/ja_khan_gir) | Urgent (critical) vulnerabilities |

Use the following **email subject** format:

```text
[SECURITY] backend_to_ml — <short description>
```

Example: `[SECURITY] backend_to_ml — outdated dependency in month-05`

---

## What to include in the report

Please provide as much detail as possible:

### 1. Vulnerability type

- [ ] Unsafe practice in a code example (SQL injection, XSS, command injection)
- [ ] CVE in a dependency
- [ ] Infrastructure / build pipeline
- [ ] Secret leak (.env, key, token)
- [ ] Other: _________________

### 2. Location

- **File path**: `src/month-XX/example-Y.md`
- **Line number** (if known)
- **Dependency name and version** (for CVEs)

### 3. Reproduction steps

```text
1. ...
2. ...
3. Expected outcome: ...
4. Actual outcome (the vulnerability): ...
```

### 4. Impact assessment

- **Who is affected?** (readers of the book, people using the code in production, etc.)
- **What harm is possible?** (data leak, code execution, RCE, etc.)
- **Severity (your estimate)**: Critical / High / Medium / Low

### 5. Suggested fix (optional)

If you have an idea — how would you fix it?

---

## Response time (SLA)

We aim to respond within the following windows:

| Stage | Time | Description |
|-------|------|-------------|
| First response | within 48 hours | Acknowledge receipt |
| Initial assessment | within 7 days | Validate the report and assess severity |
| Fix or plan | based on severity: |
| └ Critical | within 7 days | Hot patch |
| └ High | within 14 days | Priority fix |
| └ Medium | within 30 days | Next release |
| └ Low | within 90 days | When convenient |

> Note: This is a **personal project** (single maintainer), so responses may occasionally be delayed. Thank you for your patience.

---

## Coordinated disclosure

We follow **coordinated (responsible) disclosure**:

1. **You report** — we acknowledge.
2. **We discuss together** — a fix is prepared.
3. **Fix is released** — a new version/commit is announced.
4. **Public disclosure** — the vulnerability is published **after** the fix lands.
5. **Credit** — your name (if you wish) is listed in the acknowledgements.

### Embargo period

By default, **90 days** (industry standard). Can be shortened if the vulnerability is already being exploited in the wild.

---

## Hall of Fame

Researchers who responsibly disclose vulnerabilities receive special thanks:

- Your name / GitHub username will be added to the "Security Researchers" section of `README.md` (if you wish).
- Credit is given in CHANGELOG or release notes.
- A personal thank-you message via Telegram.

> Note: There is **no bug bounty** (no paid reward) — this is a free, open-source project. But your contribution is **valued** and remembered.

---

## Additional resources

- [OWASP Top 10](https://owasp.org/Top10/) — most common web vulnerabilities
- [Python Security Best Practices](https://snyk.io/learn/python-security/)
- [OWASP ML Top 10](https://owasp.org/www-project-machine-learning-security-top-10/) — ML model security
- [Snyk Vulnerability DB](https://security.snyk.io/) — dependency checks

---

## FAQ

<details>
<summary><b>What kinds of "security" issues can exist in a book project?</b></summary>

- Use of dangerous functions like `eval()` or `pickle.load()` in code examples without warning
- Real API keys, passwords, or tokens leaking into examples
- Outdated or vulnerable dependencies in `pyproject.toml`
- Broken or malicious external links (man-in-the-middle attack vector)
- Incorrect recommendations for safely deploying ML models in production

</details>

<details>
<summary><b>I found something small — is it a security issue?</b></summary>

If you're unsure — **just email us**. Sending a private email is **always better** than opening a public issue. We can decide together: if it's a regular bug, we'll invite you to open a public issue; if it's truly a security matter, we'll follow the protocol.

</details>

<details>
<summary><b>Can I report anonymously?</b></summary>

Yes. You can send email from an anonymous address (e.g., ProtonMail). However, **a contact channel** is needed if you want a response.

</details>

---

<div align="center">

**We care about security together.**

[← Back to README](README.md) · [CONTRIBUTING.md](CONTRIBUTING.md) · [Code of Conduct](CODE_OF_CONDUCT.md)

</div>
