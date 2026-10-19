# Service OS AI skills

Read-only Service OS mobile investigation for **Codex and Cursor**. Supply **FE ID and Job ID**; Job ID is the app taskId. Incident time, issue description and screenshots are additional context. The skill first checks Firebase and **mobile** Coralogix. It asks for a debug log only after dashboard investigation leaves insufficient evidence.

## Install and access

Requires macOS/Linux, Python 3.9+, Git, access to this private repository, a local Codex or Cursor client with skills support, and your own Firebase/Coralogix access. No mobile source checkout is needed. This bundle does not grant access or supply credentials, connectors, a custom MCP server, task APIs or shared browser sessions.

```bash
git clone https://github.com/ishwar260596/service-os-ai-skills.git
cd service-os-ai-skills
./service-os-skills install
./service-os-skills doctor
```

Before the initial PR merges, check out `codex/service-os-initial-skill` after cloning. After merge, install from main.

Open this cloned folder as a workspace in Codex or Cursor and start a new conversation. Installation configures routing for the current directory by default. To use another workspace, including one without application code:

```bash
./service-os-skills install --project /absolute/path/to/workspace
```

The installer copies the bundle to `~/.local/share/service-os-skills/bundle`, symlinks the skill into `~/.agents/skills/service-os`, and the CLI into `~/.local/bin/service-os-skills`. The source clone can be removed after installation. Ensure `~/.local/bin` is on PATH to invoke the CLI by name; otherwise use `~/.local/share/service-os-skills/bundle/service-os-skills`.

It merges a **Codex UserPromptSubmit hook** into `~/.codex/hooks.json` and appends an owned block to the selected workspace's `AGENTS.md`. It creates an always-apply Cursor routing rule at `.cursor/rules/service-os.mdc`. Existing unrelated hooks and instructions are preserved; conflicting skill links or Cursor rules are refused. Existing hooks.json gets a one-time backup. Only install hooks from code you trust; complete the client's normal trust prompt. Managed environments can disable hooks; doctor cannot override or prove client trust.

Codex keyword routing is user-level where hooks are supported/trusted. Cursor keyword routing applies in each registered workspace; register every workspace you use. For cross-workspace Cursor routing without registering folders, copy the routing instruction in [client-setup.md](docs/client-setup.md) into Cursor User Rules. Local installations do not provision cloud/remote agents.

## Invoke

Cursor: type `/`, choose **service-os**, then send:

```text
/service-os inspect
FE ID: 1289
Job ID: 434834
```

Codex native skill selection uses `$service-os`:

```text
$service-os inspect
FE ID: 1289
Job ID: 434834
```

The installed routing also handles plain `/service-os inspect` and Service OS/service-os/serviceos keywords. Codex's slash picker is not claimed to register an arbitrary custom command. Routing is a required instruction, not optional selection; it still depends on the client actually loading the configured hook/rule. Verify with [pilot-checks.md](docs/pilot-checks.md).

Only the IDs are mandatory. Without incident time, search cumulatively from one fixed current time: **24 hours → 48 hours → 3 days → 7 days → 30 days → 45 days**, stopping when sufficient evidence is found or a verified access/retention limit is reached. Supplied incident times anchor historical searches. The latest Firebase observed release/build is checked live on every investigation; actual incident version and required version remain separate.

## Debugging access

The AI discovers available authenticated tools first. If unavailable, it asks you to sign in to the Service OS Firebase/mobile Coralogix dashboards through browser tools supported by your client. A tool listed in the client does not establish authentication. If the client has no browser/dashboard connector, report that limitation and arrange supported access; the skill cannot create browser control. Do not share passwords or OTPs in chat.

After accessible remote checks are insufficient, the AI explains the gap and asks you to attach an app debug `.txt` file covering the incident. Continue in the same conversation with the same IDs. It does not ask for a log at intake. See [SKILL.md](skills/service-os/SKILL.md).

## Updates and learning

```bash
./service-os-skills update
./service-os-skills doctor
./service-os-skills uninstall
```

`update` clones canonical **main** into a temporary directory, validates and replaces the stable copied bundle. It does not depend on the original clone still existing and does not pull over your authoring changes. It refreshes merged knowledge only; it does not poll or run in the background. Restart clients afterward. Do not use update before the initial implementation is merged to main. `doctor` checks local files/configuration and reports revision; authentication and live-client behavior still need the manual checks it prints.

New issue types/material findings generate draft knowledge PRs via the agent's authorized GitHub tools or Git + authenticated `gh`. This is agent-driven, not a daemon. [Learning policy](skills/service-os/references/learning.md) defines deduplication, sanitization, confidence and failure handling. Reviewer: **@ishwar260596**. No automatic merge. GitHub write access is separate from read-only production investigation. Without publication access a local candidate is retained and the blocker reported.

## Validation and limits

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests
```

These checks validate packaging, routing outputs, installation preservation and update behavior. They do not establish live Firebase/Coralogix access, end-to-end Codex/Cursor behavior, production diagnoses or automatic PR permissions. Run [pilot-checks.md](docs/pilot-checks.md) before team rollout. Architecture/logging references are dated source snapshots, not evidence that a specific release is deployed. No historical sample incident is marked solved in this bundle.

Keep this repository private: references contain internal architecture and telemetry details. Do not commit raw logs, customer data, credentials or signed URLs. `CODEOWNERS` names the reviewer; branch review enforcement depends on GitHub settings and plan.
