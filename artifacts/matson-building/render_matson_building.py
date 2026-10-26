"""Review renders for matson-building.glb (thin wrapper over the Transbay batch kit).

    blender -b --python render_matson_building.py

Runs tools/landmark-kit/render.py: four elevations, top, aerial, aerial-night
and matson-building-contact-sheet.png, written next to this file.
"""

import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..", "..", "tools", "landmark-kit", "render.py")
sys.argv = [sys.argv[0], "--", "--glb", os.path.join(HERE, "matson-building.glb"), "--out", HERE,
            "--prefix", "matson-building", "--samples", "24"]
runpy.run_path(KIT, run_name="__main__")
