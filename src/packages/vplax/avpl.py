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

    def from_cue(self, cue) -> bool:
        is_ok = self._from_cue(cue) == ""
        return is_ok

    def _read_playlist(self, path:str) -> bool:
        if path:
            lines = self.read_file(path)
        else:
            lines = ["#"]
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

    def _from_cue(self, cue) -> str:
        self.songs = []
        path = cue.get_path()
        nfiles, fname, items = cue.file_info()
        nfiles = int(nfiles)
        if nfiles < 1:
            return f"No files at: {path}"
        if nfiles > 2:
            return f"More than one file at: {path}"
        res = []
        ori_sec, last = 1, 1
        for track_num_str, fields in items:
            assert int(track_num_str) > 0, f"Invalid track number: {track_num_str}"
            index = fields["INDEX"][0][:-len(":xx")]
            sec_ref = playlistmeta.convert_hhmmss(index) + ori_sec
            d_time = sec_ref - last
            dct = self._from_cue_item(fields)
            #print(":::", dct, "seconds:", sec_ref, "; time:", d_time)
            dct["@path"] = fname
            if self.songs:
                self.songs[-1]["TIME"] = d_time
            self.songs.append(dct)
            last = sec_ref
        return ""

    def _from_cue_item(self, fields:dict):
        title = fields["TITLE"]
        performer = fields["PERFORMER"]
        dct = {
            "NAME": title,
            "ATST": performer,
            "TIME": "?",
        }
        return dct


if __name__ == "__main__":
    print("Import me!")
