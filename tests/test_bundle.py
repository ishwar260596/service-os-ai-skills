import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class BundleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='service-os-test-')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.user = self.base / 'user'
        self.project = self.base / 'workspace with spaces'
        self.project.mkdir()
        self.env = dict(os.environ, SERVICE_OS_USER_ROOT=str(self.user))

    def cli(self, *args, source=ROOT, ok=True):
        p = subprocess.run(['python3', str(source / 'service-os-skills'), *args],
                           env=self.env, text=True, capture_output=True)
        if ok:
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        else:
            self.assertNotEqual(p.returncode, 0)
        return p

    def test_install_reinstall_preserve_and_uninstall(self):
        agents = self.project / 'AGENTS.md'
        agents.write_text('# Existing instructions\nDo not remove me.\n')
        hook = self.user / '.codex/hooks.json'
        hook.parent.mkdir(parents=True)
        unrelated = {'hooks': [{'type': 'command', 'command': 'existing-hook'}]}
        hook.write_text(json.dumps({'hooks': {'UserPromptSubmit': [unrelated]}}))
        self.cli('install', '--project', str(self.project))
        self.cli('install', '--project', str(self.project))
        installed = self.user / '.local/share/service-os-skills/bundle'
        self.assertEqual((self.user / '.agents/skills/service-os').resolve(), (installed / 'skills/service-os').resolve())
        self.assertEqual(agents.read_text().count('<!-- service-os-skills:start -->'), 1)
        self.assertIn('Do not remove me.', agents.read_text())
        entries = json.loads(hook.read_text())['hooks']['UserPromptSubmit']
        self.assertEqual(len(entries), 2)
        self.assertIn(unrelated, entries)
        self.cli('doctor')
        self.cli('uninstall', source=installed)
        self.assertIn('Do not remove me.', agents.read_text())
        self.assertNotIn('service-os-skills:start', agents.read_text())
        self.assertEqual(json.loads(hook.read_text())['hooks']['UserPromptSubmit'], [unrelated])
        self.assertFalse((self.user / '.agents/skills/service-os').is_symlink())

    def test_conflict_refused_before_mutation(self):
        conflict = self.user / '.agents/skills/service-os'
        conflict.mkdir(parents=True)
        (conflict / 'mine').write_text('keep')
        self.cli('install', '--project', str(self.project), ok=False)
        self.assertEqual((conflict / 'mine').read_text(), 'keep')
        self.assertFalse((self.project / 'AGENTS.md').exists())
        self.assertFalse((self.user / '.local/share/service-os-skills/bundle').exists())

    def test_cursor_conflict_and_invalid_json_are_preserved(self):
        rule = self.project / '.cursor/rules/service-os.mdc'
        rule.parent.mkdir(parents=True)
        rule.write_text('my rule')
        self.cli('install', '--project', str(self.project), ok=False)
        self.assertEqual(rule.read_text(), 'my rule')
        rule.unlink()
        hook = self.user / '.codex/hooks.json'
        hook.parent.mkdir(parents=True)
        hook.write_text('{invalid')
        self.cli('install', '--project', str(self.project), ok=False)
        self.assertEqual(hook.read_text(), '{invalid')
        self.assertFalse((self.user / '.local/share/service-os-skills/bundle').exists())

    def test_malformed_marker_order_refused_before_install(self):
        agents = self.project / 'AGENTS.md'
        original = '<!-- service-os-skills:end -->\n<!-- service-os-skills:start -->\n'
        agents.write_text(original)
        self.cli('install', '--project', str(self.project), ok=False)
        self.assertEqual(agents.read_text(), original)
        self.assertFalse((self.user / '.local/share/service-os-skills/bundle').exists())
        self.assertFalse((self.user / '.codex/hooks.json').exists())

    def test_uninstall_preflights_all_workspaces(self):
        later = self.base / 'z-workspace'
        later.mkdir()
        self.cli('install', '--project', str(self.project))
        self.cli('install', '--project', str(later))
        original = (self.project / 'AGENTS.md').read_text()
        (later / '.cursor/rules/service-os.mdc').write_text('unrelated replacement')
        self.cli('uninstall', ok=False)
        self.assertEqual((self.project / 'AGENTS.md').read_text(), original)
        self.assertTrue((self.project / '.cursor/rules/service-os.mdc').exists())
        self.assertTrue((self.user / '.agents/skills/service-os').is_symlink())

    def test_prompt_routing_and_untrusted_input(self):
        for prompt in ['/service-os inspect', '$service-os', 'Service OS issue', 'serviceos', 'SERVICE-OS']:
            result = subprocess.run(['python3', str(ROOT / 'hooks/route_prompt.py')],
                                    input=json.dumps({'prompt': prompt + ' SECRET_SENTINEL'}),
                                    text=True, capture_output=True, check=True)
            context = json.loads(result.stdout)['hookSpecificOutput']['additionalContext']
            self.assertIn('name: service-os', context)
            self.assertNotIn('SECRET_SENTINEL', context)
        for prompt in ['hello', 'microserviceos', 'service-oscar']:
            result = subprocess.run(['python3', str(ROOT / 'hooks/route_prompt.py')],
                                    input=json.dumps({'prompt': prompt}), text=True, capture_output=True, check=True)
            self.assertEqual(json.loads(result.stdout), {})

    def test_update_from_installed_copy_after_source_removed(self):
        source = self.base / 'source'
        shutil.copytree(ROOT, source, ignore=shutil.ignore_patterns('.git', '__pycache__'))
        def git(*args):
            return subprocess.check_output(['git', *args], cwd=source, stderr=subprocess.STDOUT, text=True)
        git('init', '-b', 'main')
        git('config', 'user.name', 'Synthetic Test')
        git('config', 'user.email', 'synthetic@example.invalid')
        git('add', '.')
        git('commit', '-m', 'initial')
        remote = self.base / 'remote.git'
        subprocess.run(['git', 'clone', '--bare', str(source), str(remote)], check=True, capture_output=True)
        self.cli('install', '--project', str(self.project), source=source)
        state_path = self.user / '.local/share/service-os-skills/state.json'
        state = json.loads(state_path.read_text())
        state['remote'] = str(remote)
        state_path.write_text(json.dumps(state))
        (source / 'VERSION').write_text('0.2.1\n')
        git('add', 'VERSION')
        git('commit', '-m', 'update')
        git('push', str(remote), 'main')
        shutil.rmtree(source)
        installed = self.user / '.local/share/service-os-skills/bundle'
        self.cli('update', source=installed)
        self.assertEqual((installed / 'VERSION').read_text(), '0.2.1\n')
        self.cli('doctor', source=installed)
        self.assertTrue((self.project / '.cursor/rules/service-os.mdc').exists())


if __name__ == '__main__':
    unittest.main()
