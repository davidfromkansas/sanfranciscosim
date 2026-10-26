"""Review renders of the exported 100-first.glb (thin wrapper over the batch kit).

    blender -b --python render_100_first.py [-- --only aerial]

Runs tools/landmark-kit/render.py on the shipped GLB: four elevations, top,
day aerial, night aerial and 100-first-contact-sheet.png, written here.
"""

import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..", "..", "tools", "landmark-kit", "render.py")
extra = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
sys.argv = [sys.argv[0], "--", "--glb", os.path.join(HERE, "100-first.glb"), "--out", HERE,
            "--prefix", "100-first", "--samples", "24"] + extra
runpy.run_path(KIT, run_name="__main__")
