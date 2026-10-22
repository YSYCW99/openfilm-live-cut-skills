"""Validate distributable skill entrypoints and release manifests."""
from pathlib import Path
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    'live-highlight-selector', 'content-compliance-scanner', 'audio-restore',
    'broll-matcher', 'platform-copy-writer', 'mg-overlay-planner',
}

def validate(root=ROOT):
    errors = []
    found = {p.parent.name for p in root.glob('*/SKILL.md')}
    if found != EXPECTED:
        errors.append(f'Skill set mismatch: missing={EXPECTED-found}, unexpected={found-EXPECTED}')
    for name in sorted(EXPECTED):
        folder = root / name
        try:
            content = (folder / 'SKILL.md').read_text(encoding='utf-8')
            match = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)', content, re.S)
            if not match:
                raise ValueError('Missing YAML frontmatter')
            front = yaml.safe_load(match.group(1))
            manifest = yaml.safe_load((folder / 'manifest.yml').read_text(encoding='utf-8'))
            if not isinstance(front, dict) or not isinstance(manifest, dict):
                raise ValueError('Metadata must be YAML mappings')
            if set(front) - {'name', 'description', 'license', 'allowed-tools', 'metadata'}:
                raise ValueError('Unsupported SKILL.md frontmatter field')
            if front.get('name') != name or manifest.get('name') != name:
                raise ValueError('Name differs from folder')
            for document in (front, manifest):
                if not isinstance(document.get('description'), str) or not document['description'].strip():
                    raise ValueError('Missing description')
            version = front.get('metadata', {}).get('version')
            if not isinstance(version, str) or not re.fullmatch(r'\d+\.\d+\.\d+', version):
                raise ValueError('metadata.version must be a semver string')
            if manifest.get('version') != version:
                raise ValueError('Manifest version mismatch')
            if not isinstance(manifest.get('tags'), list) or not manifest['tags']:
                raise ValueError('Manifest tags must be a nonempty list')
            if not content[match.end():].strip():
                raise ValueError('Missing instructions')
            print(f'PASS {name} {version}')
        except (OSError, ValueError, yaml.YAMLError) as exc:
            errors.append(f'{name}: {exc}')
    if errors:
        for error in errors:
            print(f'FAIL {error}', file=sys.stderr)
        return 1
    print('Validated all six skill packages.')
    return 0

if __name__ == '__main__':
    raise SystemExit(validate())
