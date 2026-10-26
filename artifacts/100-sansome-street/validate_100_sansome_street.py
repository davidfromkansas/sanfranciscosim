"""Contract validation of 100-sansome-street.glb: a thin wrapper around the shared kit.

    blender -b --python validate_100_sansome_street.py [-- --glb FILE --out FILE]

Runs tools/landmark-kit/validate.py with this building's target height and
manifest anchor; it factory-resets, re-imports only the exported GLB and writes
validation.json. Extra arguments after `--` override the defaults.
"""

import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..", "..", "tools", "landmark-kit", "validate.py")
ARGS = ["--glb", os.path.join(HERE, "100-sansome-street.glb"), "--out", os.path.join(HERE, "validation.json"),
        "--height", "58.2", "--budget", "3000", "--anchor", "-122.4004726,37.7915113"]

extra = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
sys.argv = [KIT, "--"] + extra + ARGS  # first occurrence wins, so extras override
runpy.run_path(KIT, run_name="__main__")
