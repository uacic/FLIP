"""
some functions that will convert binary images to pngs

Jacob Long
2019-11-14
"""

import multiprocessing
import os

import PIL
from PIL import Image

def bin_to_png(input_path, output_dir):
    """converts a single .bin image to png"""
    # written by David Moller
    try:
        raw_data = open(input_path, 'rb').read()
        img_size = (1936, 1216)
        img = PIL.Image.frombytes('L', img_size, raw_data, 'raw')
        savename = os.path.basename(input_path)[:-4] + '.png'
        output_path = os.path.join(output_dir, savename)
        img.save(output_path)
        print(savename, "converted")
    except Exception as e:
        print(f"{input_path}: {e}")

def convert_dir(input_dir, output_dir):
    """converts all the .bin images in a directory to .png"""

    for f in os.listdir(input_dir):
        if f.endswith(".bin"):
            bin_to_png(os.path.join(input_dir, f), output_dir)

def convert_dirs(input_base_dir, output_base_dir, processes=-1):
    """calls convert dir in a new process on each
    of the subdirectories in a given directory"""

    # finding all directories in the given dir
    dirs_to_process = []
    output_dirs = []
    with os.scandir(input_base_dir) as it:
        for entry in it:
            if entry.is_dir():
                dirs_to_process.append(entry.path)
                # create sub dir of the same name as the input
                output_dir = os.path.join(output_base_dir, entry.name)
                os.mkdir(output_dir)
                output_dirs.append(output_dir)

    # using the max number of processes if none are specified
    if processes < 1:
        processes = multiprocessing.cpu_count()

    # opening a new process for each directory found
    with multiprocessing.Pool(multiprocessing.cpu_count()) as p:
        p.map(convert_dir, dirs_to_process, output_dirs)

    print("Finished converting to pngs in", directory)

if __name__ == "__main__":

    filepath = r"W:\GeneratedData\F013B2\PS2\Test"

    convert_dirs(filepath)
    
