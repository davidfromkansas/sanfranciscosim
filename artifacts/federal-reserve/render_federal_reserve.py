"""Review renders of the exported federal-reserve.glb (thin wrapper over the batch kit).

    blender -b --python render_federal_reserve.py [-- --only aerial]

Runs tools/landmark-kit/render.py on the shipped GLB: four elevations, top,
day aerial, night aerial and federal-reserve-contact-sheet.png, written here.
"""

import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..", "..", "tools", "landmark-kit", "render.py")
extra = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
sys.argv = [sys.argv[0], "--", "--glb", os.path.join(HERE, "federal-reserve.glb"), "--out", HERE,
            "--prefix", "federal-reserve", "--samples", "24"] + extra
runpy.run_path(KIT, run_name="__main__")
