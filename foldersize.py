import os
import sys
import argparse

class Printer:
    def __init__(self):
        self.buffer = 0
    def print(self, text):
        if self.buffer > 0:
            sys.stdout.write(f"\x1b[{self.buffer}D")
            sys.stdout.write("\x1b[K")
        self.buffer = len(text)
        sys.stdout.write(text)
        sys.stdout.flush()
    def clear(self):
        if self.buffer > 0:
            sys.stdout.write(f"\x1b[{self.buffer}D")
            sys.stdout.write("\x1b[K")
            sys.stdout.flush()

def sanitize_string(string):
    sanitized_string = ""
    for c in string:
        if ord(c) > 128:
            c = "?"
            break
        sanitized_string += c
    return sanitized_string

def measure_folder_size(folder, printer : Printer, sum = 0, count = 0):
    for file in os.listdir(folder):
        fullpath = os.path.join(folder, file)
        if os.path.isdir(fullpath):
            partial_sum, partial_count = measure_folder_size(fullpath, printer, sum, count)
            sum = partial_sum
            count = partial_count
        else:
            stat = os.stat(fullpath)
            sum += stat.st_size
            if count % 100 == 0:
                megabytes = f"{(sum/(1024*1024)):.02f}"
                truncated_string = fullpath[-80:]
                if len(truncated_string) != len(fullpath):
                    truncated_string = "..."+truncated_string
                # remove unicode because length issues
                sanitize_string(truncated_string)
                printer.print(megabytes + " " + sanitized_string)
            count += 1
    return sum, count

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    options = parser.parse_args()

    fullpath = os.path.realpath(options.path)
    if not os.path.isdir(fullpath):
        raise Exception("Must specify directory")
    for obj in os.listdir(fullpath):
        fullobjpath = os.path.join(fullpath, obj)
        if os.path.isdir(obj):
            print(fullobjpath, end=" ")
            sys.stdout.flush()
            printer = Printer()
            size, count = measure_folder_size(fullobjpath, printer)
            printer.clear()
            print(f"/{size/(1024*1024):.02f}")
        else:
            stat = os.stat(fullobjpath)
            print(fullobjpath, stat.st_size)
    print(unicode_strings)
if __name__ == "__main__":
    main()