"""Contract validation for pge-general-office.glb (thin wrapper over the Transbay batch kit).

    blender -b --python validate_pge_general_office.py

Runs tools/landmark-kit/validate.py with this building's target height (79.8 m)
and manifest anchor (-122.3968490,37.7923850), writing validation.json next to this file.
"""

import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..", "..", "tools", "landmark-kit", "validate.py")
sys.argv = [sys.argv[0], "--", "--glb", os.path.join(HERE, "pge-general-office.glb"),
            "--out", os.path.join(HERE, "validation.json"),
            "--height", "79.8", "--anchor", "-122.3968490,37.7923850"]
runpy.run_path(KIT, run_name="__main__")
