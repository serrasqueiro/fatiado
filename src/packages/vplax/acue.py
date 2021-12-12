# (c)2021  Henrique Moreira

""" acue -- CUE playlists alternate (simplified) module
"""

# pylint: disable=missing-function-docstring


from vplax.playlistmeta import PlayListMeta
from vplax.keystring import KeyString


KEYING_WITHIN_TRACK = (
    "TITLE",
    "PERFORMER",
    "INDEX",
)


class ACue(PlayListMeta):
    """ cue playlist """
    # pylint: disable=unbalanced-tuple-unpacking

    def __init__(self, path=""):
        super().__init__(path)
        info = self._read_playlist(path)

    def _read_playlist(self, path:str) -> bool:
        lines = self.read_file(path)
        state = ""
        a_track = None
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
            pstring = KeyString(right)
            rvalue = pstring.lean()
            #print(":", key, "=", right)
            if key == "FILE":
                state = key
                info[key] = rvalue
                assert pstring.is_lean(), f"(FILE) String not lean: {right}"
            elif key == "REM":
                if state:
                    continue
                assert pstring.is_lean(), f"(REM) String not lean: {right}"
                first = rvalue[0]
                rest = rvalue[1:]
                if first in info[key]:
                    info[key][first].append(rest)
                else:
                    info[key][first] = [rest]
            elif state:
                assert pstring.is_lean(), f"({key}) String not lean: {right}"
                if key == "TRACK":
                    info["@tracks"].append([rvalue, {}])
                    a_track = rvalue
                elif key in KEYING_WITHIN_TRACK:
                    assert a_track, f"Bogus {key}: {key}={right}"
                    hang = info["@tracks"][-1][1]
                    hang[key] = rvalue
            elif not state:
                assert pstring.is_lean(), f"({key}) String not lean: {right}"
                info["@head"][key] = rvalue
        self._metadata = info
        return True


if __name__ == "__main__":
    print("Import me!")
