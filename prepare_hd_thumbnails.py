"""Prepare denser geometry only for static renders; do not change web meshes."""
from pathlib import Path
import json,numpy as np
import build_iteration3 as b

def main():
 out=b.ROOT.parent/'thumbnail-work';out.mkdir(exist_ok=True)
 report=[]
 for project in b.PROJECTS:
  key=project['id']
  if key=='porsche':
   source=b.BASE/'porsche 924 board/porsche dashboard 1 complet.stl'
   v,f=b.read_mesh(source)
   reg=json.loads((b.ROOT/'PORSCHE-REGISTRATION.json').read_text());coords=json.loads((b.ROOT/'PORSCHE-COORDINATES.json').read_text())
   v=v@np.array(reg['rotation'])+reg['translation']
   v=(v@np.array(coords['orientation'])-coords['centre_after_rotation'])/coords['scale']
  else:
   source=b.BASE/project['source'];v,f=b.read_mesh(source)
   v-=v.mean(0);_,basis=np.linalg.eigh(np.cov(v[::max(1,len(v)//40000)].T));v=v@basis[:,[2,1,0]]
   v-=(v.min(0)+v.max(0))/2;v/=np.ptp(v,axis=0).max()
  # A five times finer spatial grid than the interactive mesh.
  cells=np.round(v/.0015).astype(np.int32);_,inverse=np.unique(cells,axis=0,return_inverse=True)
  counts=np.bincount(inverse);verts=np.column_stack([np.bincount(inverse,weights=v[:,a])/counts for a in range(3)])
  faces=inverse[f];faces=faces[(faces[:,0]!=faces[:,1])&(faces[:,1]!=faces[:,2])&(faces[:,0]!=faces[:,2])]
  _,keep=np.unique(np.sort(faces,axis=1),axis=0,return_index=True);faces=faces[keep]
  yaw,pitch={'case':(3.79,-.35),'civic':(3.32,-.15)}.get(key,(.18,-.12))
  ry=np.array([[np.cos(yaw),0,np.sin(yaw)],[0,1,0],[-np.sin(yaw),0,np.cos(yaw)]])
  rx=np.array([[1,0,0],[0,np.cos(pitch),-np.sin(pitch)],[0,np.sin(pitch),np.cos(pitch)]])
  verts=verts@ry.T@rx.T
  verts-=(verts.min(0)+verts.max(0))/2
  np.savez(out/f'{key}.npz',vertices=verts.astype(np.float32),faces=faces.astype(np.int32))
  report.append({'id':key,'source':str(source),'render_faces':len(faces)})
  print(key,len(faces),'triangles for HD render',flush=True)
 (out/'manifest.json').write_text(json.dumps(report,indent=2))

if __name__=='__main__':main()
