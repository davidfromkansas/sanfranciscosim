set -e
B=/Applications/Blender.app/Contents/MacOS/Blender
"$B" -b --python render_ab.py -- input/hiram-johnson-state-office-building.glb renders/in > /tmp/ab_in.log 2>&1
"$B" -b --python render_ab.py -- hiram-johnson-state-office-building.optimized.glb renders/out > /tmp/ab_out.log 2>&1
echo AB_RENDERS_DONE
