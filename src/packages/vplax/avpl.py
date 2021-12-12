# (c)2021  Henrique Moreira

""" avpl -- VUPlayer lists alternate (simplified) module
"""

# pylint: disable=missing-function-docstring

import vplax.playlistmeta as playlistmeta


class AVPL(playlistmeta.APlay):
    """ VUPlayer alternate list """
    def __init__(self, path=""):
        super().__init__(path)
        self._read_playlist(path)

    def _read_playlist(self, path:str) -> bool:
        lines = self.read_file(path)
        if lines[0].startswith("#"):
            head, tail = lines[0], lines[1:]
            self._line += 1
        else:
            head, tail = "", lines
        self._add_lines(tail)
        return True

    def _add_lines(self, alist:list):
        for line in alist:
            self._line += 1
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
