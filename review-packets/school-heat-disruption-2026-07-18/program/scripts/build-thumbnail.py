"""Compatibility wrapper for the school-heat construct-validation dossier.

The previous thumbnail repeated a false top-one robustness claim. The dossier
now owns the corrected hero and all article figures.
attestation_chain: ai-first.
"""

from __future__ import annotations

import runpy
from pathlib import Path


if __name__ == "__main__":
    runpy.run_path(
        str(Path(__file__).with_name("build-figure-dossier.py")),
        run_name="__main__",
    )
