"""Fresh-scene contract validation of 201-mission.glb (thin wrapper over the batch kit).

    blender -b --python validate_201_mission.py

Runs tools/landmark-kit/validate.py with this building's target height (135.9 m),
triangle budget (27,000) and manifest anchor; writes validation.json here.
"""

import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..", "..", "tools", "landmark-kit", "validate.py")
sys.argv = [sys.argv[0], "--", "--glb", os.path.join(HERE, "201-mission.glb"),
            "--out", os.path.join(HERE, "validation.json"),
            "--height", "135.9", "--anchor", "-122.3949073,37.7911895"]
runpy.run_path(KIT, run_name="__main__")
