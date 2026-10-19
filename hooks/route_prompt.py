#!/usr/bin/env python3
"""Codex UserPromptSubmit: add routing context only for explicit Service OS terms."""
import json
from pathlib import Path
import re
import sys


def route(prompt):
    return bool(re.search(r'(?<![\w])(?:service[\s-]+os|serviceos)(?![\w])', prompt, re.I))


if __name__ == '__main__':
    try:
        data = json.load(sys.stdin)
        prompt = data.get('prompt', '')
        if not isinstance(prompt, str):
            raise ValueError('prompt must be text')
        if route(prompt):
            skill = Path(__file__).resolve().parents[1] / 'skills/service-os/SKILL.md'
            # Add maintained instructions, never echo user/log content as developer instructions.
            print(json.dumps({'hookSpecificOutput': {'hookEventName': 'UserPromptSubmit',
                'additionalContext': 'Apply the installed Service OS skill for this request.\n' + skill.read_text()}}))
        else:
            print('{}')
    except (ValueError, OSError) as error:
        print(f'Service OS routing unavailable: {error}', file=sys.stderr)
        sys.exit(1)
