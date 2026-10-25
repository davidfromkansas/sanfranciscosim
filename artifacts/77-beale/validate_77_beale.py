"""Contract validation for 77-beale.glb (thin wrapper over the Transbay batch kit).

    blender -b --python validate_77_beale.py

Runs tools/landmark-kit/validate.py with this building's target height (150.0 m)
and manifest anchor (-122.3957540,37.7917820), writing validation.json next to this file.
"""

import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..", "..", "tools", "landmark-kit", "validate.py")
sys.argv = [sys.argv[0], "--", "--glb", os.path.join(HERE, "77-beale.glb"),
            "--out", os.path.join(HERE, "validation.json"),
            "--height", "150.0", "--anchor", "-122.3957540,37.7917820"]
runpy.run_path(KIT, run_name="__main__")
