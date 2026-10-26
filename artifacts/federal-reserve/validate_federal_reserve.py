"""Fresh-scene contract validation of federal-reserve.glb (thin wrapper over the batch kit).

    blender -b --python validate_federal_reserve.py

Runs tools/landmark-kit/validate.py with this building's target height (63.1 m),
triangle budget (27,000) and manifest anchor; writes validation.json here.
"""

import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..", "..", "tools", "landmark-kit", "validate.py")
sys.argv = [sys.argv[0], "--", "--glb", os.path.join(HERE, "federal-reserve.glb"),
            "--out", os.path.join(HERE, "validation.json"),
            "--height", "63.1", "--anchor", "-122.3955200,37.7930020"]
runpy.run_path(KIT, run_name="__main__")
