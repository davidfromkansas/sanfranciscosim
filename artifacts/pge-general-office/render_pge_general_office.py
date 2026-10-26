"""Review renders for pge-general-office.glb (thin wrapper over the Transbay batch kit).

    blender -b --python render_pge_general_office.py

Runs tools/landmark-kit/render.py: four elevations, top, aerial, aerial-night
and pge-general-office-contact-sheet.png, written next to this file.
"""

import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..", "..", "tools", "landmark-kit", "render.py")
sys.argv = [sys.argv[0], "--", "--glb", os.path.join(HERE, "pge-general-office.glb"), "--out", HERE,
            "--prefix", "pge-general-office", "--samples", "24"]
runpy.run_path(KIT, run_name="__main__")
