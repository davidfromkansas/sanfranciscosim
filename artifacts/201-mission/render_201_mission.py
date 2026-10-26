"""Review renders of the exported 201-mission.glb (thin wrapper over the batch kit).

    blender -b --python render_201_mission.py [-- --only aerial]

Runs tools/landmark-kit/render.py on the shipped GLB: four elevations, top,
day aerial, night aerial and 201-mission-contact-sheet.png, written here.
"""

import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..", "..", "tools", "landmark-kit", "render.py")
extra = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
sys.argv = [sys.argv[0], "--", "--glb", os.path.join(HERE, "201-mission.glb"), "--out", HERE,
            "--prefix", "201-mission", "--samples", "24"] + extra
runpy.run_path(KIT, run_name="__main__")
