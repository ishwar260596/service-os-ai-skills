# Client setup and documented behavior

Verified documentation on 2026-10-19:

- [Codex skills](https://learn.chatgpt.com/docs/build-skills): user skills in `~/.agents/skills`; symlinks supported; explicit `$service-os` invocation.
- [Codex hooks](https://learn.chatgpt.com/docs/hooks): `~/.codex/hooks.json`, `UserPromptSubmit`, developer `additionalContext`, client trust and policy requirements.
- [Cursor skills](https://prod.cursor.com/docs/skills): shared `~/.agents/skills`, project `.cursor/skills`, native `/service-os` skill selection.
- [Cursor rules](https://prod.cursor.com/docs/rules): `.cursor/rules/*.mdc` with `alwaysApply: true`; global User Rules configured through Customize → Rules.

The installer uses the shared skill directory to avoid duplicate skill discoveries. It installs a Codex routing hook and a Cursor always-apply rule for each chosen workspace. It does not silently change Cursor's private settings database. The project's AGENTS block is an additional explicit routing instruction. These are separate from connectors and auth.

For global Cursor User Rules, add this instruction through the supported UI:

```text
Whenever the user invokes /service-os, $service-os, Service OS, service-os or serviceos, you MUST read and apply ~/.agents/skills/service-os/SKILL.md before responding. For incident investigation only FE ID and Job ID are mandatory. Check Firebase latest release and mobile Coralogix first. Request a debug log only after dashboard checks leave insufficient evidence. General Service OS questions do not require incident IDs.
```

Alternatively register each workspace with `service-os-skills install --project /absolute/workspace`. Restart/start a fresh conversation. Verify that rule/hook activation appears in the actual client, not just on disk. In a managed client that disables hooks, use the workspace AGENTS instructions and explicit native skill invocation and report the routing limitation. Do not bypass client trust or enterprise policies.

Older `service-os-inspect` installations are not deleted automatically. Explicitly select `service-os`; uninstall or archive the older skill yourself if it causes ambiguous selection. Each team member uses their own authorized sessions. A source download alone does not share the author's dashboard access.
