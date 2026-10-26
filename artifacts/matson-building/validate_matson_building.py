"""Contract validation for matson-building.glb (thin wrapper over the Transbay batch kit).

    blender -b --python validate_matson_building.py

Runs tools/landmark-kit/validate.py with this building's target height (73.0 m)
and manifest anchor (-122.3965080,37.7926550), writing validation.json next to this file.
"""

import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..", "..", "tools", "landmark-kit", "validate.py")
sys.argv = [sys.argv[0], "--", "--glb", os.path.join(HERE, "matson-building.glb"),
            "--out", os.path.join(HERE, "validation.json"),
            "--height", "73.0", "--anchor", "-122.3965080,37.7926550"]
runpy.run_path(KIT, run_name="__main__")
