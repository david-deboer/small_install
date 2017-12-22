#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
import argparse
import os
import shutil
import json
import sys
import datetime

"""
This scheme is a light-weight install package for small stuff.
If the 'package' has a .py extension, it just copies it to the python (often miniconda2) bin.  Note the
    bin is set in '.paths.json'.
If a package needs more files, use the .paths.json-code_path.py stuff.  This puts code_path.py path into
    the site-packages directory
If there is no extensions given:
    if there is a python file of that name, it will make a bash wrapper and copy that to the local bin
    otherwise it just copies that to the local bin
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


def rerun(e=None):
    if e is None:
        e = 'R'
    else:
        e = e + ' and r'
    print("===> {}e-run 'small_install.py small_install' <===".format(e))
    sys.exit()


# ############################################################################################################# #
ap = argparse.ArgumentParser()
ap.add_argument('module', help="Name of module to install.  If no extension, makes/installs wrapper of python.")
ap.add_argument('-i', '--invoke_name', help="Name of bash wrapper or rename in bin.", default='default')
ap.add_argument('-u', '--uninstall', help="Uninstall the module (i.e. rm from bin).", action='store_true')
ap.add_argument('--version', help='Python version installed under. [2.7]', default='2.7')
args = ap.parse_args()

site_packages_path = os.path.expanduser('~/miniconda2/lib/python' + args.version + '/site-packages')
path_file = os.path.expanduser('~/.paths.json')
base_bin_path = None

if os.path.exists(path_file):
    with open(path_file, 'r') as f:
        PTH = json.load(f)
    base_bin_path = os.path.expanduser(PTH['small_install_bin'])
    base_bin_pypath = os.path.expanduser(PTH['small_install_pybin'])

if args.module == 'small_install':
    si_print("Installing 'small_install'")
    # Install .paths.json
    if base_bin_path is None:
        si_print('Writing {}'.format(path_file))
        base_bin_path = '~/bin'
        base_bin_pypath = '~/miniconda2/bin'
        s = '{{\n\t"small_install_bin": "{}",\n'.format(base_bin_path)
        s += '\t"small_install_pybin": "{}"\n}}\n'.format(base_bin_pypath)
        with open(path_file, 'w') as f:
            f.write(s)
        print("===> Check if this file is correct.  Edit if not. <===")
        print(s)
        rerun()
    else:
        si_print("{} exists and will be used for small_install.".format(path_file))
    # Install code_path.py
    if site_packages_path not in sys.path:
        si_print("{} is not in your python sys.path.".format(site_packages_path))
        rerun('Fix path')
    si_cp('code_path.py', site_packages_path)
    # Check pypath
    if not os.path.exists(base_bin_pypath):
        si_print("{} does not exist.".format(base_bin_pypath))
        rerun('Fix path')
    if base_bin_pypath not in sys.path:
        si_print("{} is not in your python sys.path.".format(base_bin_pypath))
        rerun('Fix path')
    # Check bin path
    if not os.path.exists(base_bin_path):
        si_print("{} does not exist.".format(base_bin_path))
        rerun('Fix path')
    if base_bin_path not in os.getenv('PATH'):
        si_print("Add {} to your PATH environment.".format(base_bin_path))


if base_bin_path is None or not os.path.exists(os.path.join(site_packages_path, 'code_path.py')):
    rerun()

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
