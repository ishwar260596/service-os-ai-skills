#!/usr/bin/env python3
"""Validate packaging and local Markdown references without third-party dependencies."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def validate(root=ROOT):
    skill = root / 'skills/service-os/SKILL.md'
    text = skill.read_text()
    assert text.startswith('---\n') and '\n---\n' in text[4:], 'Missing frontmatter'
    assert re.search(r'^name: service-os$', text, re.M), 'Wrong skill name'
    assert re.search(r'^description: .+', text, re.M), 'Missing description'
    for path in root.rglob('*.md'):
        if '.git' in path.parts:
            continue
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', path.read_text()):
            if '://' in target or target.startswith('#'):
                continue
            local = (path.parent / target.split('#')[0]).resolve()
            assert local.is_relative_to(root.resolve()), f'Reference escapes bundle: {path}: {target}'
            assert local.exists(), f'Broken reference: {path}: {target}'
    assert (root / 'hooks/route_prompt.py').is_file()
    assert (root / 'skills/service-os/agents/openai.yaml').is_file()
    print('Bundle structure and local links valid')


if __name__ == '__main__':
    validate()
