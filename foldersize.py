import os
import argparse

def measure_folder_size(folder):
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    options = parser.parse_args()

    fullpath = os.path.realpath(options.path)
    if not os.path.isdir(fullpath):
        raise Exception("Must specify directory")
    for obj in os.listdir(fullpath):
        stat = os.stat(os.path.join(fullpath, obj))
        objpath = os.path.join(fullpath, obj)
        print(obj, stat.st_size)
if __name__ == "__main__":
    main()