#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import argparse
import os
import shutil
import json
import sys
import datetime
import code_path

"""
This scheme is a light-weight install package for small stuff.
If the 'package' has a .py extension, it just copies it to the python (often miniconda2) bin.  Note the
    bin is set in '.paths.json'.
If a package needs more files, use the .paths.json-code_path.py stuff.
If there is no extensions given:
    if there is a python file of that name, it will make a bash wrapper and copy that to the "local" bin
If the .paths.json and code_path.py stuff isn't installed, it tries to set it up for you when you install
    this installer
"""

log_file = os.path.expanduser('~/.small_install_log.txt')
if os.path.exists(log_file):
    checking_log = os.stat(log_file)
    if checking_log.st_size > 10 * 1024 * 1024:
        print("{} is large ({})".format(log_file, checking_log.st_size))


def si_print(v, only_log=False, ):
    if not only_log:
        print(v)
    logTime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    v = v + ' ' * (85 - len(v)) + logTime
    with open(log_file, 'a') as f:
        print(v, file=f)


def si_cp(local, path, remote='default'):
    if remote.lower() == 'default':
        remote = local
    remote = os.path.join(os.path.expanduser(path), remote)
    shutil.copy(local, remote)
    slog = 'copying:  {} {}'.format(local, remote)
    si_print(slog, only_log=True)


def si_rm(path, remote):
    remote = os.path.join(os.path.expanduser(path), remote)
    os.remove(remote)
    slog = 'removing:  {}'.format(remote)
    si_print(slog, only_log=True)


def si_wrapper(module, invoke):
    py_script = os.path.join(os.getcwd(), module + '.py')
    si_print("Making wrapper for {}".format(py_script), only_log=True)
    nargs = 0
    with open(py_script, 'r') as fp:
        for line in fp:
            if 'add_argument' in line:
                nargs += 1

    with open(invoke, 'w') as fp:
        fp.write('#! /bin/sh\n')
        s = py_script

        for i in range(1, nargs + 1):
            if i > 9:
                s += (' ${%d}') % (i)
            else:
                s += (' $%d') % (i)
        fp.write(s + '\n')

    os.chmod(py_script, 0744)
    os.chmod(invoke, 0744)


def rerun():
    print("===> Re-run 'small_install.py small_install' <===")
    sys.exit()


# ############################################################################################################# #
ap = argparse.ArgumentParser()
ap.add_argument('module', help="Name of module to install.  If no extension, makes/installs wrapper of python.")
ap.add_argument('-i', '--invoke_name', help="Name of bash wrapper or rename in bin.", default='default')
ap.add_argument('-u', '--uninstall', help="Uninstall the module (i.e. rm from bin).", action='store_true')
args = ap.parse_args()

path_file = os.path.expanduser('~/.paths.json')
if os.path.exists(path_file):
    with open(path_file, 'r') as f:
        PTH = json.load(f)
    base_bin_path = os.path.expanduser(PTH['small_install_bin'])
    base_bin_pypath = os.path.expanduser(PTH['small_install_pybin'])

if args.module == 'small_install':
    si_print("Installing 'small_install'")
    # Install .paths.json
    if os.path.exists(path_file):
        si_print("{} exists.".format(path_file))
    else:
        si_print('Writing {}'.format(path_file))
        base_bin_path = '~/bin'
        base_bin_pypath = '~/miniconda2/lib/python2.7/site-packages'
        s = '{{\n\t"small_install_bin": "{}",\n'.format(base_bin_path)
        s += '\t"small_install_pybin": "{}"\n}}\n'.format(base_bin_pypath)
        with open(path_file, 'w') as f:
            f.write(s)
        print("===> Check if this file is correct.  Edit if not. <===")
        print(s)
        rerun()
    # Check pypath
    if not os.path.exists(base_bin_pypath):
        print("{} does not exist.  Edit the path or create the directory.".format(base_bin_pypath))
        rerun()
    if base_bin_pypath not in sys.path:
        print("{} is not in your python sys.path.  Edit the path.".format(base_bin_pypath))
        rerun()
    # Install code_path.py
    si_cp('code_path.py', base_bin_pypath)
    si_print("Setting up 'code_path.py'.")
    # Check bin path
    if not os.path.exists(base_bin_path):
        print("{} does not exist.  Edit the path or create the directory.".format(base_bin_path))
        print("If you edit the path, you will need to re-install 'small_install.py small_install'")
    if base_bin_path not in os.getenv('PATH'):
        print("Add {} to your PATH environment.".format(base_bin_path))


module_parse = args.module.split('.')
if args.invoke_name == 'default':
    args.invoke_name = args.module


if len(module_parse) == 2 and module_parse[1] == 'py':
    if args.uninstall:
        si_rm(base_bin_pypath, args.invoke_name)
    else:
        si_cp(args.module, base_bin_pypath, args.invoke_name)
elif len(module_parse) == 1:
    if args.uninstall:
        si_rm(base_bin_path, args.invoke_name)
    else:
        if os.path.exists(args.module + '.py'):
            local_name = args.invoke_name
            si_wrapper(args.module, args.invoke_name)
        elif os.path.exists(args.module):
            local_name = args.module
        else:
            local_name = None

        if local_name is not None:
            si_cp(local_name, base_bin_path, args.invoke_name)
else:
    si_print("Invalid module name:  {}".format(args.module))
