from __future__ import absolute_import, division, print_function
import os.path
import sys
import json
#  be sure to put this in the bin directory.
#  e.g. in ~/miniconda2/bin


def set(project_name):
    path_file = os.path.expanduser('~/.paths.json')
    if os.path.exists(path_file):
        with open(path_file, 'r') as f:
            path_data = json.load(f)
        try:
            sys_path = os.path.expanduser(path_data.get(project_name))
            sys.path.append(sys_path)
            return sys_path
        except KeyError:
            print("{} not found.".format(project_name))
            return None
    print("{} not found.".format(path_file))
    return None


def show():
    path_file = os.path.expanduser('~/.paths.json')
    if os.path.exists(path_file):
        with open(path_file, 'r') as f:
            path_data = json.load(f)
            for k in path_data.keys():
                print("{:20s}:  {}".format(k, os.path.expanduser(path_data[k])))
