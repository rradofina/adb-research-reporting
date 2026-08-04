"""Review-topic discovery and loading.

Constitutional basis
--------------------
CONSTITUTION.md §2.7 (review provenance track), §11 (reproducibility from a
clean clone).

A review program is any directory containing a `review.json` manifest and an
evidence module. The factory finds them by scanning the repository rather than
by a hardcoded list, so adding a topic is adding a folder — the property that
makes the second review cheap and the tenth review possible.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from dataclasses import dataclass
from pathlib import Path

MANIFEST = "review.json"

# Directories that will never hold a review, skipped so discovery stays fast.
SKIP = {"node_modules", ".git", ".cache", ".next", "__pycache__", "tmp",
        "dist", "outputs", "figures", "_archive"}


@dataclass
class Review:
    slug: str
    root: Path
    manifest: dict

    @property
    def title(self) -> str:
        return self.manifest.get("title", self.slug)

    @property
    def evidence_module(self) -> str:
        return self.manifest.get("evidence_module", "evidence_data")

    @property
    def artifacts_dir(self) -> Path:
        return self.root / self.manifest.get("artifacts_dir", ".")

    _cached_module = None

    def _module(self):
        """Import the topic's evidence module once and memoize it."""
        if self._cached_module is not None:
            return self._cached_module
        path = self.root / f"{self.evidence_module}.py"
        if not path.exists():
            raise FileNotFoundError(
                f"{self.slug}: no evidence module at {path}")
        spec = importlib.util.spec_from_file_location(
            f"_review_{self.slug}", path)
        if spec is None or spec.loader is None:
            raise ImportError(f"{self.slug}: cannot load {path}")
        module = importlib.util.module_from_spec(spec)
        # The evidence module may import siblings by bare name.
        sys.path.insert(0, str(self.root))
        try:
            spec.loader.exec_module(module)
        finally:
            sys.path.pop(0)
        self._cached_module = module
        return module

    def load_records(self) -> list[dict]:
        """The topic's EVIDENCE list."""
        records = getattr(self._module(), "EVIDENCE", None)
        if records is None:
            raise AttributeError(
                f"{self.slug}: {self.evidence_module}.py defines no EVIDENCE")
        return records

    def references(self) -> list[str]:
        """The topic's REFERENCES list, or empty when it defines none."""
        return list(getattr(self._module(), "REFERENCES", []) or [])

    def path(self, name: str) -> Path:
        """A factory-managed artifact path inside the topic folder."""
        return self.root / name


def repo_root(start: Path | None = None) -> Path:
    here = (start or Path(__file__)).resolve()
    for parent in [here, *here.parents]:
        if (parent / ".git").exists():
            return parent
    return here.parent


def discover(root: Path | None = None) -> list[Review]:
    """Find every review program under the repository root."""
    base = root or repo_root()
    found: list[Review] = []
    for path in _walk(base):
        manifest_path = path / MANIFEST
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        slug = manifest.get("slug") or path.name
        found.append(Review(slug=slug, root=path, manifest=manifest))
    return sorted(found, key=lambda r: r.slug)


def _walk(base: Path):
    stack = [base]
    while stack:
        current = stack.pop()
        try:
            entries = list(current.iterdir())
        except OSError:
            continue
        if any(e.name == MANIFEST for e in entries):
            yield current
            continue          # a review does not nest another review
        for entry in entries:
            if entry.is_dir() and entry.name not in SKIP \
                    and not entry.name.startswith("."):
                stack.append(entry)


def load(slug: str | None = None, root: Path | None = None) -> Review:
    """Load one review by slug, or the only one if there is exactly one."""
    reviews = discover(root)
    if not reviews:
        raise SystemExit("No review programs found (no review.json anywhere).")
    if slug:
        for review in reviews:
            if review.slug == slug:
                return review
        names = ", ".join(r.slug for r in reviews)
        raise SystemExit(f"No review {slug!r}. Known: {names}")
    if len(reviews) == 1:
        return reviews[0]
    names = ", ".join(r.slug for r in reviews)
    raise SystemExit(f"Several reviews exist; pass --review. Known: {names}")
