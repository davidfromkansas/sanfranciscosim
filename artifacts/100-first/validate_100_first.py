"""Fresh-scene contract validation of 100-first.glb (thin wrapper over the batch kit).

    blender -b --python validate_100_first.py

Runs tools/landmark-kit/validate.py with this building's target height (136.25 m),
triangle budget (27,000) and manifest anchor; writes validation.json here.
"""

import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..", "..", "tools", "landmark-kit", "validate.py")
sys.argv = [sys.argv[0], "--", "--glb", os.path.join(HERE, "100-first.glb"),
            "--out", os.path.join(HERE, "validation.json"),
            "--height", "136.25", "--anchor", "-122.3977206,37.7891952"]
runpy.run_path(KIT, run_name="__main__")
