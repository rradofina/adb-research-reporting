"""Rebuild the validated social-protection hero.

The source of truth is ``build-figure-dossier.py`` so the standalone thumbnail
entry point cannot restore the retired country-ranking graphic.
attestation_chain: ai-first.
"""

from pathlib import Path
import runpy


module = runpy.run_path(str(Path(__file__).with_name("build-figure-dossier.py")))
module["thumbnail"]()
print("Built validated social-protection thumbnail.")
