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

    def file_info(self) -> tuple:
        """ Returns indication of file ("1", "0", "+"),
        the filename and the track listing, if only one file.
        """
        files = self._metadata["@files"]
        if not files:
            return "0", "", []
        is_one = len(files) == 1
        if not is_one:
            return "+", "", []
        what, cont = files[0]
        tracks = [(tup[0][1], tup[1]) for tup in cont]
        return "1", what, tracks

    def _read_playlist(self, path:str) -> bool:
        lines = self.read_file(path)
        state = ""
        a_track = None
        info = {
            "REM": {},
            "@files": [],	# list of files, when there is more than one file
            "@head": {},
            "@tail": None,
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
            if key == "FILE":
                state = key
                if key not in info:
                    info[key] = [rvalue]
                else:
                    info[key].append(rvalue)
                info["@files"].append((rvalue[0], []))
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
                    track_num = int(rvalue[0])
                    track_struct = [[track_num, rvalue[0], rvalue[1]], {}]
                    info["@files"][-1][1].append(track_struct)
                    a_track = info["@files"][-1][1][-1][1]
                elif key in "INDEX":
                    assert a_track, f"Bogus {key}: {key} {right}"
                    idx_num, a_time = rvalue
                    if idx_num == "00":
                        key = "INDEX_00"
                    else:
                        assert idx_num == "01"
                    hang = a_track
                    assert key not in hang, f"Duplicate key, line {idx}: {key} {right}"
                    hang[key] = (a_time,)
                elif key in KEYING_WITHIN_TRACK:
                    assert isinstance(a_track, dict), f"Bogus {key}: {key}={right}"
                    hang = a_track
                    hang[key] = right
            elif not state:
                assert pstring.is_lean(), f"({key}) String not lean: {right}"
                info["@head"][key] = rvalue
        self._metadata = info
        return True


if __name__ == "__main__":
    print("Import me!")
