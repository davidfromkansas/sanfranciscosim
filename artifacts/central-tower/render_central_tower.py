"""Review renders of central-tower.glb: a thin wrapper around the shared kit.

    blender -b --python render_central_tower.py [-- --samples 16 --only aerial,night]

Runs tools/landmark-kit/render.py on the exported GLB (re-imported into an
empty scene): four true-compass elevations, top, aerial, night aerial and
central-tower-contact-sheet.png, written next to this script. Extra arguments
after `--` override the defaults.
"""

import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..", "..", "tools", "landmark-kit", "render.py")
ARGS = ["--glb", os.path.join(HERE, "central-tower.glb"), "--out", HERE, "--prefix", "central-tower", "--samples", "24"]

extra = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
sys.argv = [KIT, "--"] + extra + ARGS  # first occurrence wins, so extras override
runpy.run_path(KIT, run_name="__main__")
