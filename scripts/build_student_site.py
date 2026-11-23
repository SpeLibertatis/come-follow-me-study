"""Copy the reviewed student deployment manifest into a fresh directory."""
import argparse
from pathlib import Path, PurePosixPath
from shutil import copyfile

MANIFEST = Path('deploy/student-files.txt')


def read_manifest(root):
    entries = []
    for line in (root / MANIFEST).read_text(encoding='utf-8').splitlines():
        name = line.strip()
        if not name or name.startswith('#'):
            continue
        p = PurePosixPath(name)
        safe_name = name == p.as_posix() and not p.is_absolute() and all(
            part.isascii() and all(ch.isalnum() or ch in '._-' for ch in part)
            and not part.startswith('.') for part in p.parts)
        allowed = (
            (p.parent == PurePosixPath('.') and p.suffix in {'.html', '.css', '.js'})
            or (p.parent == PurePosixPath('lessons') and p.suffix == '.html')
            or (p.parent in {PurePosixPath('assets'), PurePosixPath('assets/lessons')}
                and p.suffix in {'.svg', '.webp'})
            or (p.parent == PurePosixPath('handouts') and p.suffix == '.pdf')
            or p in {PurePosixPath('design/tokens.css'), PurePosixPath('PRIVACY.md')}
        )
        if not safe_name or not allowed or name in entries:
            raise ValueError(f'Invalid or duplicate student path: {name!r}')
        entries.append(name)
    if not {'index.html', 'lessons.html'} <= set(entries):
        raise ValueError('The homepage and reusable QR collection must both be listed.')
    return entries


def build(root, output):
    root = root.resolve()
    if output.exists() or output.is_symlink():
        raise FileExistsError(f'Output must be a fresh directory: {output}')
    entries = read_manifest(root)
    for name in entries:
        source = root / name
        if not source.is_file() or source.resolve() != source:
            raise ValueError(f'Missing file or symbolic link: {name!r}')
    output.mkdir(parents=True, exist_ok=False)
    for name in entries:
        target = output / name
        target.parent.mkdir(parents=True, exist_ok=True)
        copyfile(root / name, target)
    return len(entries)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True, help='New directory to populate')
    args = parser.parse_args()
    print(f'Packaged {build(Path(__file__).resolve().parents[1], args.output)} reviewed student files.')
