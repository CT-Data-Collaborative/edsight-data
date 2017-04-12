import os
import filecmp
import difflib

from collections import namedtuple

BASE_OLD_DATA_DIR = './crawls/33017'
BASE_NEW_DATA_DIR = './data'

Mismatch = namedtuple('Mismatch', ['dir', 'filename'])

subdir_names = next(os.walk(BASE_OLD_DATA_DIR))[1]

subdir_file_names = {d: os.listdir(os.path.join(BASE_OLD_DATA_DIR, d)) for d in subdir_names}

mismatches = []
file_not_found = []

for dir, files in subdir_file_names.items():
    for f in files:
        if not f == '.DS_Store':
            file_a = os.path.join(BASE_OLD_DATA_DIR, dir, f)
            file_b = os.path.join(BASE_NEW_DATA_DIR, dir, f)
            try:
                if not filecmp.cmp(file_a, file_b, shallow=False):
                    mismatches.append(Mismatch(dir, f))
                    print(len(mismatches))
            except FileNotFoundError:
                file_not_found.append(file_a)

total_files = 0
for dir, files in subdir_file_names.items():
    for f in files:
        total_files +=1


mismatches_dict = {}
for m in mismatches:
    if m.dir not in mismatches_dict:
        mismatches_dict[m.dir] = []
    mismatches_dict[m.dir].append(m.filename)