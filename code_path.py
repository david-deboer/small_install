from __future__ import absolute_import, division, print_function
import os.path
import sys
import json
#  be sure to put this in the bin directory.
#  e.g. in ~/miniconda2/bin


def set(project_name):
    with open(os.path.expanduser('~/.paths.json'), 'r') as f:
        path_data = json.load(f)
    sys_path = os.path.expanduser(path_data.get(project_name))
    sys.path.append(sys_path)
    return sys_path


def show():
    with open(os.path.expanduser('~/.paths.json'), 'r') as f:
        path_data = json.load(f)
    for k in path_data.keys():
        print("{:20s}:  {}".format(k, os.path.expanduser(path_data[k])))
