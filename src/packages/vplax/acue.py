# (c)2021  Henrique Moreira

""" acue -- CUE playlists alternate (simplified) module
"""

# pylint: disable=missing-function-docstring


from vplax.playlistmeta import PlayListMeta


class ACue(PlayListMeta):
    """ cue playlist """
    # pylint: disable=unbalanced-tuple-unpacking

    def __init__(self, path=""):
        super().__init__(path)
        info = self._read_playlist(path)

    def _read_playlist(self, path:str) -> bool:
        lines = self.read_file(path)
        state = ""
        info = {
            "REM": {},
            "@head": {},
            "@tail": None,
            "@tracks": [],
        }
        for line in lines:
            self._line += 1
            idx = self._line
            is_ok, words = self._key_split(line)
            if not words:
                continue	# ignore empty line
            msg = words[0]
            assert is_ok, msg
            key, right = words
            assert key, f"Bad CUE line, {idx}: {line}"
            if key == "FILE":
                state = key
                info[key] = right
            #print(":", key, "=", right)
        self._metadata = info
        return True


if __name__ == "__main__":
    print("Import me!")
