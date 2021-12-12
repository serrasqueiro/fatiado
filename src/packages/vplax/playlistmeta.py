# (c)2021  Henrique Moreira

""" playlistmeta -- generic playlist meta-data
"""

# pylint: disable=missing-function-docstring, no-self-use


class APlay():
    """ Abstract class for any playlist """
    def __init__(self, path="", encoding="latin-1"):
        self._path = path
        self._line = 0
        if encoding in ("latin-1",):
            encoding = "ISO-8859-1"
        self._encoding = encoding
        self.songs = []

    def get_path(self):
        return self._path

    def read_file(self, path):
        enc_in = self._encoding
        lines = open(path, "r", encoding=enc_in).read().splitlines()
        return lines


class PlayListMeta(APlay):
    """ cue playlist """
    def __init__(self, path=""):
        super().__init__(path)
        self._metadata = {}

    def information(self) -> dict:
        """ Returns meta-data information """
        return self._metadata

    def _key_split(self, astr:str) -> tuple:
        """ Splits a playlist line, e.g. CUE,
		TRACK 01 AUDIO
		TITLE "School"
        """
        line = astr.replace("\t", " ")
        left = line.strip()
        if not left:
            return True, tuple()
        is_ok = not left.startswith('"')
        if not is_ok:
            return False, (f"Invalid line: {astr}",)
        words = left.split(" ", maxsplit=1)
        key = None
        if len(words) == 2:
            key, right = words
        else:
            right = words[0]
        if right.startswith('"') and right.endswith('"'):
            right = right[1:-1].strip()
        return True, (key, right)


if __name__ == "__main__":
    print("Import me!")
