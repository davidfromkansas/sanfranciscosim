"""Review renders for 123-mission.glb (thin wrapper over the Transbay batch kit).

    blender -b --python render_123_mission.py

Runs tools/landmark-kit/render.py: four elevations, top, aerial, aerial-night
and 123-mission-contact-sheet.png, written next to this file.
"""

import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..", "..", "tools", "landmark-kit", "render.py")
sys.argv = [sys.argv[0], "--", "--glb", os.path.join(HERE, "123-mission.glb"), "--out", HERE,
            "--prefix", "123-mission", "--samples", "24"]
runpy.run_path(KIT, run_name="__main__")
