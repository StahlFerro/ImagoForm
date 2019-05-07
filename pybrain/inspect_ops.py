import os
import string
from random import choices
from pprint import pprint
from urllib.parse import urlparse

from PIL import Image
from apng import APNG
from colorama import init, deinit
from hurry.filesize import size, alternative

from .config import IMG_EXTS, STATIC_IMG_EXTS, ANIMATED_IMG_EXTS


def _inspect_image(animage_path):
    """Returns information of an animted GIF/APNG"""
    filename = str(os.path.basename(animage_path))
    abspath = os.path.abspath(animage_path)
    workpath = os.path.dirname(abspath)
    ext = str.lower(os.path.splitext(filename)[1])

    if os.getcwd() != workpath:
        os.chdir(workpath)

    frame_count = 0
    fps = 0
    duration = 0
    fsize = size(os.stat(filename).st_size, system=alternative)
    # fsize = 0
    width = height = 0
    loop_duration = 0
    extension = ''

    if ext == '.gif':
        try:
            gif: Image = Image.open(filename)
        except Exception:
            return
        if gif.format != 'GIF' or not gif.is_animated:
            raise Exception(f"The chosen GIF ({filename}) is not an animated GIF!")
        width, height = gif.size
        frame_count = gif.n_frames
        # pprint(gif.info)
        durations = []
        for f in range(0, gif.n_frames):
            gif.seek(f)
            durations.append(gif.info['duration'])
        duration = sum(durations) / len(durations)
        fps = 1000.0 / duration
        loop_duration = frame_count / fps
        extension = 'GIF'

    elif ext == '.png':
        try:
            apng: APNG = APNG.open(filename)
        except Exception:
            pass
        frames = apng.frames
        frame_count = len(frames)
        if frame_count <= 1:
            raise Exception(f"The chosen PNG ({filename}) is not an APNG!")
        png_one, controller_one = frames[0]
        # pprint(png_one.__dict__)
        # pprint(controller_one.__dict__)
        extension = 'APNG'
        width = png_one.width
        height = png_one.height
        duration = controller_one.delay
        fps = 1000.0 / duration
        loop_duration = frame_count / fps

    image_info = {
        "name": filename,
        "fps": fps,
        "duration": duration,
        "fsize": fsize,
        "extension": extension,
        "frame_count": frame_count,
        "absolute_url": abspath,
        "width": width,
        "height": height,
        "loop_duration": loop_duration,
    }
    return image_info


def _inspect_sequence(image_paths):
    """Returns information of a selected sequence of images"""
    abs_image_paths = [os.path.abspath(ip) for ip in image_paths if os.path.exists(ip)]
    imgs = [f for f in abs_image_paths if '.' in f and str.lower(f.split('.')[-1]) in STATIC_IMG_EXTS]
    # raise Exception("imgs", imgs)
    print("imgs count", len(imgs))
    # pprint(imgs)
    if not imgs:
        raise Exception("No images selected. Make sure the path to them are correct")
    first_img = imgs[0].split('.')[0]
    filename = os.path.basename(first_img.split('_')[0] if '_' in first_img else first_img)
    # apngs = [apng for apng in (APNG.open(i) for i in imgs) if len(apng.frames) > 1]
    # gifs = [gif for gif in (Image.open(i) for i in imgs) if gif.format == "GIF" and gif.is_animated]
    statics = [i for i in imgs if len(APNG.open(i).frames) == 1 and Image.open(i).format != "GIF"]
    print("statics count", len(statics))
    # pprint(apngs)
    # pprint(gifs)
    # if any(APNG.open(i) for i in imgs)):

    sequence_info = {
        "name": filename,
        "total": len(imgs),
        "sequences": statics,
    }
    return sequence_info