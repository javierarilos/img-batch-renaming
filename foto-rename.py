""" Copy image file (e.g. ABC.JPG) to 20180605-ABC.JPG using EXIF timestamp
    Very simple script, expects to be executed from the dir where the images are
    and the filenames from stdin.
    
    Example: ls *.JPG | python ~/mywork/img-batch-renaming/foto-rename.py
"""

import sys
import os
from itertools import chain
from shutil import copyfile, copystat
from time import strptime, strftime, mktime

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

EXIF_DATETIME=306
curr_dir = os.getcwd()
print(f'curr_dir={curr_dir}')

SUFFIX = os.getenv('SUFFIX', '')
INCLUDE_ORIGINAL = os.getenv('INCLUDE_ORIGINAL', False)


def print_exif_data(pil_image):
    print(image)
    info = image._getexif()
    for tag, value in info.items():
      key = TAGS.get(tag, tag)
      print(key + "/" + str(tag) + "> " + str(value))


def modify_mtime(fname):
    """ Change mtime and creation time, fname is a file in the current dir."""
    original_name = os.path.join(curr_dir, fname)
    ts = strptime(fname.split('-')[0], '%Y%m%d%H%M%S')
    image_time = mktime(ts)
    os.utime(original_name, (image_time, image_time))


def copy_using_exif_datetime(fname, keep_stat=True):
    original_name = os.path.join(curr_dir, fname)
    image = Image.open(original_name)
    info = image._getexif()
    dt = info.get(EXIF_DATETIME)
    ts = strptime(dt, '%Y:%m:%d %H:%M:%S')
    pref = strftime('%Y%m%d%H%M%S', ts)

    target_fname = f'{pref}-{SUFFIX}-{fname}' if SUFFIX else f'{pref}-{fname}'
    target_fullname = os.path.join(curr_dir, target_fname)
    print(f'{original_name} => {target_fname} => {target_fullname}')
    if keep_stat:
        copystat(original_name, target_fullname)
    else:
        copyfile(original_name, target_fullname)


if __name__ == '__main__':
    for fname in chain(*(l.split() for l in sys.stdin.readlines())):
        print(f'fname={fname}')
        copy_using_exif_datetime(fname)
