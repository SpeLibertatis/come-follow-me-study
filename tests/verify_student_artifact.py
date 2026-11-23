"""Verify the deployment artifact, not the repository root."""
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase, main
import sys

from verify_routes import read_routes, route_findings

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_student_site import build, read_manifest  # noqa: E402


class StudentArtifact(TestCase):
    def test_full_artifact_retains_student_routes_and_excludes_source(self):
        with TemporaryDirectory() as folder:
            output = Path(folder) / 'student-site'
            build(ROOT, output)
            manifest = read_manifest(ROOT)
            self.assertEqual(sorted(p.relative_to(output).as_posix() for p in output.rglob('*') if p.is_file()),
                             sorted(manifest))
            self.assertEqual(list(route_findings(output, read_routes(output))), [])
            self.assertEqual((output / 'index.html').read_bytes(), (output / 'lessons.html').read_bytes())
            for path in ('adventure.html', 'journal.html', 'daniel.html', 'explore.html', '2026.html', '2027.html',
                         'legacy-links.js', 'PRIVACY.md', 'lessons/hosea-joel.html', 'lessons/amos-obadiah-jonah.html'):
                self.assertIn(path, manifest)
            self.assertTrue(
                {'daniel-student-handout.pdf', 'daniel-explore-further.pdf',
                 'joel-quick-study.pdf', 'joel-deep-study.pdf',
                 'amos-quick-study.pdf', 'amos-deep-study.pdf'}
                <= {p.name for p in (output / 'handouts').glob('*.pdf')})
            for path in ('README.md', 'docs', 'tests', 'scripts', 'prototypes',
                         '.github', 'design/review', 'assets/lessons/sources.json'):
                self.assertFalse((output / path).exists(), path)
            for path in manifest:
                self.assertEqual((output / path).read_bytes(), (ROOT / path).read_bytes(), path)

    def test_requires_fresh_destination_and_rejects_unapproved_paths(self):
        with TemporaryDirectory() as folder:
            root = Path(folder) / 'checkout'
            (root / 'deploy').mkdir(parents=True)
            (root / 'index.html').write_text('lesson')
            (root / 'README.md').write_text('private to artifact, public repo')
            manifest = root / 'deploy/student-files.txt'
            dest = Path(folder) / 'candidate'
            manifest.write_text('index.html\nREADME.md\n')
            with self.assertRaises(ValueError):
                build(root, dest)
            self.assertFalse(dest.exists())
            manifest.write_text('index.html\n')
            dest.mkdir()
            (dest / 'old.html').write_text('stale')
            with self.assertRaises(FileExistsError):
                build(root, dest)


if __name__ == '__main__':
    main()
