# Getting started (about five minutes)

**Product = Natural Language Compiler** ([Natural Language Compiler (NLC)](../../TERMS.md#nlc) practice). This page is the NLC compiler docs home (`docs/nlc/compiler/`); it is not a second public roof.

1. **Install**

   Linux:

   ```bash
   curl -fsSL https://raw.githubusercontent.com/Zygotic-AI/Natural-Language-Compiler/main/scripts/install.sh | bash
   ```

   macOS:

   ```bash
   curl -fsSL https://raw.githubusercontent.com/Zygotic-AI/Natural-Language-Compiler/main/scripts/install.sh | /bin/bash
   ```

   Windows (PowerShell):

   ```powershell
   Set-ExecutionPolicy -Scope Process Bypass -Force
   irm https://raw.githubusercontent.com/Zygotic-AI/Natural-Language-Compiler/main/scripts/install.ps1 | iex
   ```

   Piped install is **global** (this user). In a terminal the installer asks **global** or **local**. Local pins the current git repo (`.nlc/hub`, `./nlc`, skills in that repo). Non-interactive: `--global` / `--local`, or `NLC_INSTALL_SCOPE=global|local`. After a local pin, PATH `nlc` in that repo execs the repo copy and passes every argument through.

2. **Open your [app repo](../../TERMS.md#adopter)** in Cursor (or work in this hub for charter/tool changes).

   From the repo root run **`./nlc`** (dashboard). See [`docs/nlc/MENU.md`](../MENU.md).

3. **`/interview`** — state the outcome; bind goals, requirements, and [knowledge domains](../../TERMS.md#knowledge-domain). Use [INTERVIEW-PATTERNS.md](INTERVIEW-PATTERNS.md) when stuck. Stop when gaps are closed or explicitly [waived](../../TERMS.md#waived). Do not emit product code in this pass.

4. **`/planit`** — load → plan → bind → generate (one artifact) → [gate](../../TERMS.md#gate) → [verify](../../TERMS.md#verify) (`./nlc verify-deep`). See [PROCESS.md](PROCESS.md).

5. **Red vs green** — in your [app repo](../../TERMS.md#adopter): `./nlc verify` (CI) and `./nlc ship-check`. Use `/verify` in the agent when [verify](../../TERMS.md#verify) fails. [Ship](../../TERMS.md#ship) needs human `Released-by:` on `CONFIRM.md`.

Adopt a new repo: [BOOTSTRAP.md](../../adoption/BOOTSTRAP.md). Words: [GLOSSARY.md](GLOSSARY.md).
