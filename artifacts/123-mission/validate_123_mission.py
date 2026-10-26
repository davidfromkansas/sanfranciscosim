"""Contract validation for 123-mission.glb (thin wrapper over the Transbay batch kit).

    blender -b --python validate_123_mission.py

Runs tools/landmark-kit/validate.py with this building's target height (124.0 m)
and manifest anchor (-122.3944470,37.7918240), writing validation.json next to this file.
"""

import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..", "..", "tools", "landmark-kit", "validate.py")
sys.argv = [sys.argv[0], "--", "--glb", os.path.join(HERE, "123-mission.glb"),
            "--out", os.path.join(HERE, "validation.json"),
            "--height", "124.0", "--anchor", "-122.3944470,37.7918240"]
runpy.run_path(KIT, run_name="__main__")
