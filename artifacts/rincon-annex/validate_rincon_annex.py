"""Fresh-scene contract validation of rincon-annex.glb (thin wrapper over the batch kit).

    blender -b --python validate_rincon_annex.py

Runs tools/landmark-kit/validate.py with this building's target height (29.7 m),
triangle budget (27,000) and manifest anchor; writes validation.json here.
"""

import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..", "..", "tools", "landmark-kit", "validate.py")
sys.argv = [sys.argv[0], "--", "--glb", os.path.join(HERE, "rincon-annex.glb"),
            "--out", os.path.join(HERE, "validation.json"),
            "--height", "29.7", "--anchor", "-122.3931571,37.7925049"]
runpy.run_path(KIT, run_name="__main__")
