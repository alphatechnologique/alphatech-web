from pathlib import Path
import runpy,sys
sys.path.insert(0,str(Path(__file__).parent))
runpy.run_path(str(Path(__file__).with_name("build_iteration3.py")),run_name="__main__")
runpy.run_path(str(Path(__file__).with_name("build_porsche_progress.py")),run_name="__main__")
runpy.run_path(str(Path(__file__).with_name("build_iteration6.py")),run_name="__main__")
runpy.run_path(str(Path(__file__).with_name("build_iteration7.py")),run_name="__main__")
runpy.run_path(str(Path(__file__).with_name("build_iteration8.py")),run_name="__main__")
runpy.run_path(str(Path(__file__).with_name("build_iteration9.py")),run_name="__main__")
