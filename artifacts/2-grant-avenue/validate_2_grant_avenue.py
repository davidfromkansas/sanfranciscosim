"""Contract validation of 2-grant-avenue.glb: a thin wrapper around the shared kit.

    blender -b --python validate_2_grant_avenue.py [-- --glb FILE --out FILE]

Runs tools/landmark-kit/validate.py with this building's target height and
manifest anchor; it factory-resets, re-imports only the exported GLB and writes
validation.json. Extra arguments after `--` override the defaults.
"""

import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..", "..", "tools", "landmark-kit", "validate.py")
ARGS = ["--glb", os.path.join(HERE, "2-grant-avenue.glb"), "--out", os.path.join(HERE, "validation.json"),
        "--height", "19.5", "--anchor", "-122.4046839,37.7871305", "--budget", "3000"]

extra = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
sys.argv = [KIT, "--"] + extra + ARGS  # first occurrence wins, so extras override
runpy.run_path(KIT, run_name="__main__")
