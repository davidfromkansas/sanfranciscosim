"""Contract validation of 700-market-street.glb: a thin wrapper around the shared kit.

    blender -b --python validate_700_market_street.py [-- --glb FILE --out FILE]

Runs tools/landmark-kit/validate.py with this building's target height, the
batch triangle cap and the manifest anchor printed by tk.run; it re-imports only
the exported GLB and writes validation.json. Extra arguments after `--` override.
"""

import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..", "..", "tools", "landmark-kit", "validate.py")
ARGS = ["--glb", os.path.join(HERE, "700-market-street.glb"), "--out", os.path.join(HERE, "validation.json"),
        "--height", "57.9", "--budget", "3000", "--anchor", "-122.4038192,37.7877278"]

extra = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
sys.argv = [KIT, "--"] + extra + ARGS  # first occurrence wins, so extras override
runpy.run_path(KIT, run_name="__main__")
