# Degenerate-sliver and loop-normal audit on a PACKED glb. The limited-dissolve
# failure documented in GLB-OPTIMIZE-PROMPT s.3 only shows up here: an annulus
# ngon re-triangulates into hairline slivers whose shared vertex sits between
# opposing normals, so the STORED normal collapses to ~0. Blender recomputes
# loop normals on import and hides it, so read the raw accessor instead.
import json, struct, sys, math
path = sys.argv[1]
data = open(path, 'rb').read()
assert data[:4] == b'glTF'
n = struct.unpack('<I', data[12:16])[0]
gltf = json.loads(data[20:20+n])
print(path, 'extensions:', gltf.get('extensionsUsed'))
prims = sum(len(m['primitives']) for m in gltf['meshes'])
print('  meshes', len(gltf['meshes']), 'primitives(draw submeshes)', prims,
      'materials', len(gltf['materials']), 'accessors', len(gltf['accessors']))
bad = 0; tot = 0
for m in gltf['meshes']:
    for p in m['primitives']:
        ai = p['attributes'].get('NORMAL')
        if ai is None: continue
        acc = gltf['accessors'][ai]
        tot += acc['count']
        mn, mx = acc.get('min'), acc.get('max')
        if mn and mx and all(abs(v) < 1e-4 for v in mn) and all(abs(v) < 1e-4 for v in mx):
            bad += acc['count']
print('  normal accessors covering', tot, 'verts; all-zero accessors:', bad)
