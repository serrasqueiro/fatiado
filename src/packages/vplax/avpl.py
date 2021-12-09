# (c)2021  Henrique Moreira

""" avpl -- VUPlayer lists alternate (simplified) module
"""

# pylint: disable=missing-function-docstring


class APlay():
    """ Abstract class for any playlist """
    def __init__(self, path=""):
        self._path = path

    def get_path(self):
        return self._path


class AVPL(APlay):
    """ VUPlayer alternate list """
    def __init__(self, path=""):
        super().__init__(path)
        self.songs = []
        self._read_playlist(path)

    def _read_playlist(self, path:str) -> bool:
        lines = data = open(path, "r").read().splitlines()
        if lines[0].startswith("#"):
            head, tail = lines[0], lines[1:]
        else:
            head, tail = "", lines
        self._add_lines(tail)
        return True

    def _add_lines(self, alist:list):
        for line in alist:
            items = line.split("\x01")
            idx = 0
            for item in items:
                idx += 1
                if idx == 1:
                    dct = {"@path": item}
                    continue
                left, right = item.split("=", maxsplit=1)
                dct[left] = right
            self.songs.append(dct)


if __name__ == "__main__":
    print("Import me!")
