"""Check the public student artifact after deployment; perform read-only GETs."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from time import sleep
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen
import uuid

from build_student_site import read_manifest

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://spelibertatis.github.io/come-follow-me-study/'
EXCLUDED = (
    'README.md', 'SECURITY.md', 'tests/verify.py', 'docs/joel-narrative-design-review.md',
    'scripts/build_handout.py', 'prototypes/daniel-visual-v1/index.html',
    'design/review/word-challenge/README.md', 'assets/lessons/sources.json',
)
CONTENT_TYPES = {
    '.html': {'text/html'},
    '.css': {'text/css'},
    '.js': {'application/javascript', 'text/javascript'},
    '.svg': {'image/svg+xml'},
    '.webp': {'image/webp'},
    '.pdf': {'application/pdf'},
}


def compare(path, expected_file, cache_key):
    location = BASE + quote(path) + '?pages-smoke=' + cache_key
    request = Request(location, headers={'User-Agent': 'Come Follow Me Pages smoke check'})
    try:
        with urlopen(request, timeout=8) as response:
            if response.geturl() != location:
                return f'unexpected redirect to {response.geturl()}'
            if expected_file is None:
                return f'expected 404, received {response.status}'
            kinds = CONTENT_TYPES.get(expected_file.suffix)
            mime = response.headers.get_content_type()
            if kinds and mime not in kinds:
                return f'unexpected Content-Type {mime}'
            expected = expected_file.read_bytes()
            if response.read(len(expected) + 1) != expected:
                return 'published bytes differ from the verified source'
    except HTTPError as error:
        if expected_file is None and error.code == 404:
            return None
        return f'HTTP {error.code}'
    except (OSError, URLError) as error:
        return str(error)
    return None


def main(attempts=3):
    allowed = {'': ROOT / 'index.html'}
    allowed.update({name: ROOT / name for name in read_manifest(ROOT)})
    checks = {**allowed, **dict.fromkeys(EXCLUDED)}
    for number in range(attempts):
        cache_key = uuid.uuid4().hex
        with ThreadPoolExecutor(max_workers=10) as pool:
            results = list(pool.map(lambda item: compare(*item, cache_key), checks.items()))
        failures = [(name, error) for name, error in zip(checks, results) if error]
        if not failures:
            print(f'Passed {len(allowed)} student URL checks and {len(EXCLUDED)} exclusion checks.')
            return 0
        if number < attempts - 1:
            print(f'{len(failures)} checks pending propagation, attempt {number + 1}/{attempts}.', flush=True)
            checks = {name: checks[name] for name, _ in failures}
            sleep(5)
    for name, error in failures:
        print(f'{name or "/"}: {error}')
    return 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--attempts', type=int, default=3, choices=(1, 2, 3))
    raise SystemExit(main(parser.parse_args().attempts))
