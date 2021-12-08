# (c)2021  Henrique Moreira

""" globdir -- Directory handling (using 'scandir')

Usage:
	adir = processors.globdir.ADir('/tmp')
	# Last entry (most recent file):
	adir.bydate()[-1][1]
        date_str = datetime.datetime.fromtimestamp(entry.stat().st_mtime).strftime("%Y-%m-%d %H:%M")

An ambiguous list is:
	adir.dir_slash() + adir.files()
"""

from os import scandir

# pylint: disable=missing-function-docstring


class GDir():
    """ Directory entries """
    def __init__(self, path="", only_ext=None):
        self._path = path
        self._exts = only_ext if only_ext else tuple()
        self._files, self._dirs = [], []
        self._by_date = []
        self.rescan()

    def rescan(self) -> bool:
        """ Rescan path """
        path = self._path if self._path else "."
        self._files, self._dirs, self._by_date = [], [], []
        try:
            entries = scandir(path)
        except FileNotFoundError:
            return False
        self._add_entries(entries)
        return True

    def files(self) -> list:
        """ Return file by alpha-name """
        return self._files

    def dirs(self) -> list:
        """ Return dir names """
        return self._dirs

    def dir_slash(self) -> list:
        """ Return dir names with a slash suffix """
        return [name + "/" for name in self._dirs]

    def files_byname(self) -> list:
        """ Return files by name (case sensitive) """
        return sorted(self._files)

    def files_bydate(self) -> list:
        """ Return files by date """
        return [name for name, _ in self._by_date]

    def bydate(self) -> list:
        """ Return file by modification date,
        as pairs: name, DirEntry
        """
        return self._by_date

    def eligible(self, entry) -> bool:
        if not self._exts:
            return entry.is_file()
        name = entry.name
        for an_ext in self._exts:
            if name.endswith(an_ext):
                return True
        return False

    def _add_entries(self, adir):
        """ Add entries
        'adir' is an iterator.
        """
        dire, dirs = [], []
        for entry in adir:
            if self.eligible(entry):
                dire.append((self._best_path(entry), entry.stat().st_mtime, entry))
            elif entry.is_dir():
                dirs.append(entry.name)
        for name, _, entry in sorted(dire, key=lambda x: x[1]):
            self._by_date.append((name, entry))
        names = sorted([entry.name for _, _, entry in dire], key=str.casefold)
        self._files += names
        self._dirs += sorted(dirs)
        return dire

    def _best_path(self, entry):
        if self._path:
            return entry.path
        # Avoid putting "./name.xyz" ("./" prefix)
        return entry.name


if __name__ == "__main__":
    print("Import me!")
