#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import argparse
import os
import shutil
import json

bin_path = os.path.expanduser('~/.paths.json')
with open(bin_path, 'r') as f:
    PTH = json.load(f)
base_bin_path = os.path.expanduser(PTH['small_install_bin'])
base_bin_pypath = os.path.expanduser(PTH['small_install_pybin'])

module_help = "Name of module -- action depends on extension:\n\texclude py:  make bash, copy to {}\n\tinclude py:  just copy file to {}"\
              .format(base_bin_path, base_bin_pypath)
ap = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
ap.add_argument('module', help=module_help)
ap.add_argument('-i', '--invoke_name', help="Name of bash wrapper. (*)", default='default')
args = ap.parse_args()

module_parse = args.module.split('.')

if len(module_parse) == 2 and module_parse[1] == 'py':
    shutil.copy(args.module, os.path.join(base_bin_pypath, args.module))
elif len(module_parse) == 1:
    if args.invoke_name == 'default':
        args.invoke_name = args.module
    py_script = os.path.join(os.getcwd(), args.module + '.py')

    nargs = 0
    fp = open(py_script, 'r')
    for line in fp:
        if 'add_argument' in line:
            nargs += 1
        # if '--' in line:
        #     nargs += 1
    fp.close()

    with open(args.invoke_name, 'w') as fp:
        fp.write('#! /bin/sh\n')
        s = py_script

        for i in range(1, nargs + 1):
            if i > 9:
                s += (' ${%d}') % (i)
            else:
                s += (' $%d') % (i)
        fp.write(s + '\n')

    os.chmod(py_script, 0744)
    os.chmod(args.invoke_name, 0744)

    shutil.copy(args.invoke_name, os.path.join(base_bin_path, args.invoke_name))
else:
    print("Invalid module name:  {}".format(args.module))
