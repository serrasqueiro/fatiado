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
   ext        Show extension -e ...
""")
    sys.exit(code if code else 0)


def run(args, instream):
    """ Main script """
    opts = {
        "verbose": 0,
        "reverse": False,
        "ext": [],
    }
    if not args:
        return None
    cmd, param = args[0], args[1:]
    while param and param[0].startswith("-"):
        if param[0] == "-e":
            opts["ext"].append(param[1])
            del param[:2]
            continue
        if param[0] == "-r":
            opts["reverse"] = True
            del param[0]
            continue
        return None
    if param:
        return None
    if cmd in ("sort",):
        code = do_sort(instream, opts)
        return code
    if cmd in ("ext",):
        code = dir_ext("", opts["ext"])
        return code
    return None


def do_sort(instream, opts):
    lines = instream.readlines()
    res = sorted_paths(lines, opts)
    for path in res:
        print(path)
    return 0


def sorted_paths(lines:list, opts):
    do_reverse = opts["reverse"]
    tups = []
    for line in lines:
        path = line.strip()
        atime = best_effort_mtime(path)
        shown = path if atime > 0 else (path + "?")
        tups.append((atime, shown))
    alist = sorted(tups, key=lambda x: x[0], reverse=do_reverse)
    return [path for _, path in alist]


def best_effort_mtime(path:str):
    try:
        atime = os.path.getmtime(path)
    except FileNotFoundError:
        atime = 0.0
    return atime


def dir_ext(path, exts:list) -> int:
    """ Dumps files with any of extension 'exts' """
    code = dir_listing(path, exts, 0)
    return code

def dir_listing(path, exts, level:int):
    if level >= 100:
        sys.stderr.write(f"Nesting too high: {level}, for: {path}")
        return -1
    adir = GDir(path, only_ext=exts)
    for name in adir.dir_slash():
        if name.startswith("."):
            continue
        dir_listing(os.path.join(path, name.rstrip("/")), exts, level + 1)
    for name in adir.files():
        shown = os.path.join(path, name) if path else name
        print(shown)
    return 0


if __name__ == "__main__":
    main()
