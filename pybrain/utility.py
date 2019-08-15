import os
import shutil
import time
import subprocess

from .config import gifsicle_exec, ABS_CACHE_PATH, CreationCriteria, SplitCriteria
# from .create_ops import create_aimg
# from .split_ops import split_aimg


def _purge_cache():
    for stuff in os.listdir(ABS_CACHE_PATH):
        stuff_path = os.path.join(ABS_CACHE_PATH, stuff)
        try:
            if os.path.isfile(stuff_path):
                os.unlink(stuff_path)
            elif os.path.isdir(stuff_path):
                shutil.rmtree(stuff_path)
        except Exception as e:
            print("e")


def _mk_temp_dir(prefix_name: str = ''):
    dirname = time.strftime("%Y%m%d_%H%M%S")
    if prefix_name:
        dirname = f"{prefix_name}_{dirname}"
    temp_dir = os.path.join(ABS_CACHE_PATH, dirname)
    os.mkdir(temp_dir)
    return temp_dir


def _unoptimize_gif(gif_path, out_dir) -> str:
    """ Perform GIF unoptimization using Gifsicle, in order to obtain the true singular frames for Splitting purposes. Returns the path of the unoptimized GIF """
    print("Performing unoptimization...")
    executable = gifsicle_exec()
    pure_gif_path = os.path.join(out_dir, os.path.basename(gif_path))
    args = [executable, "-b", "--unoptimize", gif_path, "--output", pure_gif_path]
    cmd = ' '.join(args)
    print(cmd)
    subprocess.run(cmd, shell=True)
    return pure_gif_path


def _reduce_color(gif_path, out_dir, color: int = 256) -> str:
    " Reduce the color of a gif. Overwrites the GIF "
    print("Performing color reduction...")
    executable = gifsicle_exec()
    redux_gif_path = os.path.join(out_dir, os.path.basename(gif_path))
    args = [executable, f"--colors={color}", gif_path, "--output", redux_gif_path]
    cmd = ' '.join(args)
    subprocess.run(cmd, shell=True)
    return redux_gif_path


def _delete_temp_images():
    # raise Exception(os.getcwd())
    temp_dir = os.path.abspath('temp')
    # raise Exception(os.getcwd(), temp_dir)
    # raise Exception(image_name, path)
    # os.remove(path)
    temp_aimgs = [os.path.join(temp_dir, i) for i in os.listdir(temp_dir)]
    for ta in temp_aimgs:
        os.remove(ta)
    return True


def _log(message):
    return {"log": message}


# def gs_build():
#     gifsicle_exec = os.path.abspath("./bin/gifsicle-1.92-win64/gifsicle.exe")
#     orig_path = os.path.abspath('./test/orig2/')
#     images = [os.path.abspath(os.path.join(orig_path, f)) for f in os.listdir(orig_path)]
#     out_dir = os.path.abspath('./test/')
#     criteria = CreationCriteria(fps=50, extension='gif', transparent=True, reverse=False)
#     create_aimg(images, out_dir, "sicle_test", criteria)
    

# def gs_split(gif_path: str, out_dir: str):
#     criteria = SplitCriteria(pad_count=3, is_duration_sensitive=False)
#     # pprint(criteria.__dict__)
#     split_aimg(gif_path, out_dir, criteria)


# if __name__ == "__main__":
#     gs_build()