# (c)2021  Henrique Moreira

""" dir_list -- Directory handling (uses dirlist globdir)
"""

import sys
import os.path
from dirlist.globdir import GDir

# pylint: disable=missing-function-docstring

def main():
    code = run(sys.argv[1:], sys.stdin)
    if code is None:
        print(f"""{__file__} command [options]

Commands are:
   sort       Show entries, sorted by date
""")
    sys.exit(code if code else 0)


def run(args, instream):
    """ Main script """
    if not args:
        return None
    cmd, param = args[0], args[1:]
    if param:
        return None
    if cmd in ("sort",):
        code = do_sort(instream)
        return code
    return None


def do_sort(instream):
    lines = instream.readlines()
    res = sorted_paths(lines)
    for path in res:
        print(path)
    return 0


def sorted_paths(lines:list):
    tups = []
    for line in lines:
        path = line.strip()
        atime = best_effort_mtime(path)
        shown = path if atime > 0 else (path + "?")
        tups.append((atime, shown))
    alist = sorted(tups, key=lambda x: x[1])
    return [path for _, path in alist]


def best_effort_mtime(path:str):
    try:
        atime = os.path.getmtime(path)
    except FileNotFoundError:
        atime = 0.0
    return atime


if __name__ == "__main__":
    main()
