"""Review renders of the exported rincon-annex.glb (thin wrapper over the batch kit).

    blender -b --python render_rincon_annex.py [-- --only aerial]

Runs tools/landmark-kit/render.py on the shipped GLB: four elevations, top,
day aerial, night aerial and rincon-annex-contact-sheet.png, written here.
"""

import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..", "..", "tools", "landmark-kit", "render.py")
extra = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
sys.argv = [sys.argv[0], "--", "--glb", os.path.join(HERE, "rincon-annex.glb"), "--out", HERE,
            "--prefix", "rincon-annex", "--samples", "24"] + extra
runpy.run_path(KIT, run_name="__main__")
