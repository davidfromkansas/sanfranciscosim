"""Contract validation of old-saint-marys-cathedral.glb: a thin wrapper around the shared kit.

    blender -b --python validate_old_saint_marys_cathedral.py [-- --glb FILE --out FILE]

Runs tools/landmark-kit/validate.py with this building's target height and
manifest anchor; it factory-resets, re-imports only the exported GLB and writes
validation.json. Extra arguments after `--` override the defaults.
"""

import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..", "..", "tools", "landmark-kit", "validate.py")
ARGS = ["--glb", os.path.join(HERE, "old-saint-marys-cathedral.glb"), "--out", os.path.join(HERE, "validation.json"),
        "--height", "33.65", "--budget", "3000", "--anchor", "-122.4057137,37.7928426"]

extra = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
sys.argv = [KIT, "--"] + extra + ARGS  # first occurrence wins, so extras override
runpy.run_path(KIT, run_name="__main__")
