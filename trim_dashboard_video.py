import bpy
from pathlib import Path
root=Path(__file__).parent
source=Path(r'C:\Users\MS1\Documents\Alpha tech Proyectos\porsche 924 board\videos\Dashboard v1.mp4')
scene=bpy.context.scene
editor=scene.sequence_editor_create()
movie=editor.strips.new_movie('Dashboard',str(source),channel=1,frame_start=1)
scene.render.fps=30
scene.render.resolution_x=movie.elements[0].orig_width
scene.render.resolution_y=movie.elements[0].orig_height
scene.render.resolution_percentage=100
scene.render.use_sequencer=True
scene.view_settings.view_transform='Standard'
scene.view_settings.look='None'
scene.frame_set(811)
scene.render.image_settings.file_format='PNG'
scene.render.filepath=str(root/'atperformance/assets/porsche-progress-poster.png')
bpy.ops.render.render(write_still=True)
scene.frame_start=601
scene.frame_end=840
scene.render.image_settings.media_type='VIDEO'
scene.render.ffmpeg.format='MPEG4'
scene.render.ffmpeg.codec='H264'
scene.render.ffmpeg.constant_rate_factor='HIGH'
scene.render.filepath=str(root/'atperformance/assets/porsche-dashboard-progress-20-28.mp4')
bpy.ops.render.render(animation=True)
