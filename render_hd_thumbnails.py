"""Run with Blender 5.1 --background --python; CPU rendering, no browser needed."""
from pathlib import Path
import bpy,json,numpy as np
from mathutils import Vector
root=Path(__file__).parent;work=root.parent/'thumbnail-work'
out=root/'atperformance/assets/hd';out.mkdir(exist_ok=True)
for item in json.loads((work/'manifest.json').read_text()):
 key=item['id'];data=np.load(work/f'{key}.npz');v=data['vertices'];f=data['faces']
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
 for mesh in list(bpy.data.meshes):
  if mesh.users==0:bpy.data.meshes.remove(mesh)
 mesh=bpy.data.meshes.new(key);mesh.vertices.add(len(v));mesh.vertices.foreach_set('co',v.ravel())
 mesh.loops.add(f.size);mesh.loops.foreach_set('vertex_index',f.ravel());mesh.polygons.add(len(f));mesh.polygons.foreach_set('loop_start',np.arange(len(f))*3);mesh.polygons.foreach_set('loop_total',np.full(len(f),3));mesh.update()
 mesh.polygons.foreach_set('use_smooth',np.ones(len(f),dtype=bool))
 obj=bpy.data.objects.new(key,mesh);bpy.context.collection.objects.link(obj)
 split=obj.modifiers.new('Preserve sharp edges','EDGE_SPLIT');split.split_angle=.6
 mat=bpy.data.materials.new('Satin silver');mat.diffuse_color=(.55,.59,.65,1);mat.use_nodes=True
 bsdf=mat.node_tree.nodes.get('Principled BSDF');bsdf.inputs['Base Color'].default_value=(.55,.59,.65,1);bsdf.inputs['Metallic'].default_value=.28;bsdf.inputs['Roughness'].default_value=.36;obj.data.materials.append(mat)
 camera=bpy.data.cameras.new('Camera');cam=bpy.data.objects.new('Camera',camera);bpy.context.collection.objects.link(cam);cam.location=(0,0,3);cam.rotation_euler=(0,0,0);camera.type='ORTHO'
 camera.ortho_scale=max(np.ptp(v[:,0])*1.18,np.ptp(v[:,1])*1920/1248*1.18)
 scene=bpy.context.scene;scene.camera=cam
 for name,loc,power,size in [('Key',(-1.2,1.5,2),170,2),('Fill',(1,-.2,1.8),95,1.6),('Rim',(.4,1,-1),180,1.3)]:
  light=bpy.data.lights.new(name,'AREA');light.energy=power;light.shape='DISK';light.size=size
  ob=bpy.data.objects.new(name,light);bpy.context.collection.objects.link(ob);ob.location=loc;ob.rotation_euler=(-ob.location).to_track_quat('-Z','Y').to_euler()
 scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.08,.09,.11,1);scene.world.node_tree.nodes['Background'].inputs[1].default_value=.3
 scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=20;scene.cycles.use_denoising=True
 scene.render.resolution_x=1920;scene.render.resolution_y=1248;scene.render.resolution_percentage=100
 scene.render.image_settings.file_format='PNG';scene.render.film_transparent=False
 scene.view_settings.view_transform='AgX';scene.render.filepath=str(out/f'{key}.png')
 bpy.ops.render.render(write_still=True);print('HD_READY',key,flush=True)
