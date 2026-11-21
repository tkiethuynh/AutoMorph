from pathlib import Path

p = Path("scripts/manager.py")
src = p.read_text(encoding="utf-8")

helper = '''    @staticmethod
    def _format_whats_new(v_details: dict) -> str:
        patch_info = v_details.get('patch', {}) or {}
        applied = patch_info.get('applied_patches', {}) or {}
        repos = patch_info.get('repos', []) or []
        morphe_ver = patch_info.get('morphe_desktop_version')
        lines = []
        if repos:
            short_repos = [
                r.replace('https://github.com/', '').replace('https://gitlab.com/', '')
                for r in repos
            ]
            lines.append(f"Sources: {', '.join(short_repos)}")
        if morphe_ver and morphe_ver != 'Unknown':
            lines.append(f"Morphe: v{morphe_ver}")
        if applied:
            lines.append(f"Applied patches ({len(applied)}):")
            for name in sorted(applied.keys()):
                lines.append(f"- {name}")
        return "\\n".join(lines) if lines else "Patched with AutoMorph"

'''

target_block = """                    'whatsNew': {
                        'en-US': 'new patches'
                    }"""
replacement_block = """                    'whatsNew': {
                        'en-US': self._format_whats_new(v_details)
                    }"""

assert target_block in src, "whatsNew target block not found in scripts/manager.py"
assert "    def add_package(self):\n        index = {" in src, "FDroid.add_package not found"

src = src.replace(
    "    def add_package(self):\n        index = {",
    helper + "    def add_package(self):\n        index = {",
    1,
)
src = src.replace(target_block, replacement_block, 1)
p.write_text(src, encoding="utf-8")
print("Patched scripts/manager.py successfully")
