"""Contract validation of 300-clay-street.glb: a thin wrapper around the shared kit.

    blender -b --python validate_300_clay_street.py [-- --glb FILE --out FILE]

Runs tools/landmark-kit/validate.py with this building's target height, triangle
budget and manifest anchor; it factory-resets, re-imports only the exported GLB and
writes validation.json. Extra arguments after `--` override the defaults.
"""

import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..", "..", "tools", "landmark-kit", "validate.py")
ARGS = ["--glb", os.path.join(HERE, "300-clay-street.glb"), "--out", os.path.join(HERE, "validation.json"),
        "--height", "121.3", "--budget", "5000", "--anchor", "-122.3992506,37.7956183"]

extra = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
sys.argv = [KIT, "--"] + extra + ARGS  # first occurrence wins, so extras override
runpy.run_path(KIT, run_name="__main__")
