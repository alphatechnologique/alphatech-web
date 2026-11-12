"""Run with Blender; export video-only media at original resolution and frame rate."""
import bpy,json
from pathlib import Path
root=Path(__file__).parent;assets=root/'atperformance/assets'
sources={'amg':assets/'amg-air-test.mp4','civic':assets/'civic-scan-pov.mp4'}
report={}
for key,source in sources.items():
 scene=bpy.context.scene
 if scene.sequence_editor:scene.sequence_editor_clear()
 editor=scene.sequence_editor_create();movie=editor.strips.new_movie(key,str(source),channel=1,frame_start=1)
 fps=movie.fps;frames=movie.frame_duration;w=movie.elements[0].orig_width;h=movie.elements[0].orig_height
 scene.render.fps=round(fps);scene.render.fps_base=scene.render.fps/fps
 scene.render.resolution_x=w;scene.render.resolution_y=h;scene.render.resolution_percentage=100
 scene.render.use_sequencer=True;scene.view_settings.view_transform='Standard';scene.view_settings.look='None'
 scene.render.image_settings.media_type='IMAGE';scene.render.image_settings.file_format='PNG'
 scene.frame_set(round(frames*.5));scene.render.filepath=str(assets/f'{key}-poster-native.png');bpy.ops.render.render(write_still=True)
 scene.frame_start=1;scene.frame_end=frames;scene.render.image_settings.media_type='VIDEO'
 scene.render.ffmpeg.format='MPEG4';scene.render.ffmpeg.codec='H264';scene.render.ffmpeg.constant_rate_factor='HIGH';scene.render.ffmpeg.audio_codec='NONE'
 target=assets/f'{key}-silent.mp4';scene.render.filepath=str(target);bpy.ops.render.render(animation=True)
 report[key]={'frames':frames,'fps':fps,'width':w,'height':h,'audio':False,'output':target.name}
 print('SILENT_READY',key,flush=True)
(root/'SILENT-VIDEO-REPORT.json').write_text(json.dumps(report,indent=2))
