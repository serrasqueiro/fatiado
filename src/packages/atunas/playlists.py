#-*- coding: utf-8 -*-
# playlists.py  (c)2021  Henrique Moreira

"""
itunes Playlists
"""

# pylint: disable=missing-function-docstring

from atunas.genarray import PDict, PArray, PKey


class Plays():
    """ Abstract/ generic Playlist class """
    def __init__(self):
        self._array = []
        self._first = None

    def get_first(self):
        """ Returns the _first (element) """
        return self._first


class Playlists(Plays):
    """ itunes Playlists - plist handler
    """
    def __init__(self, elem):
        super().__init__()
        self.elems = []
        is_ok = self._parse(elem)
        assert is_ok
        self._add_array()
        self._playlist_names = [ala.str_by_key("Name") for ala in self._array]

    def n_playlists(self) -> int:
        num = len(self._array)
        if num == 0:
            return 0
        assert self._first.get_tag() == "dict"
        return num

    def podcast_refs(self):
        """ Returns 'Podcasts' elements """
        idx = self._playlist_names.index('Podcasts')
        return self._array[idx]

    def _parse(self, elem) -> bool:
        """ Iterate through """
        anext = elem.getnext()
        while True:
            if anext is None:
                return False
            if anext.tag == "key":
                return True
            self.elems.append((anext.tag, anext))
            anext = anext.getnext()

    def _add_array(self):
        """ Iterates on existing 'elems'
        """
        items = [elem for tag, elem in self.elems if tag == "array"]
        for elems in items:
            for ala in elems.findall("./dict"):
                newobj = PDict(ala)
                if self._first is None:
                    self._first = newobj
                self._array.append(newobj)


def sample() -> str:
    astr = """
xyz = atunas.tuneinfo.TunesXML("mlib.xml")
trk = xyz.block("playlists")
pls, _, _ = trk
ply = atunas.playlists.Playlists(pls)
assert len(ply.elems) == 1
_, elems = ply.elems[0]
refp = ply.podcast_refs()
pods = PArray(refp.first_array())
item = PDict(pods.get_array()[0])	# the first Podcast array element
track_id_string = PKey(item.dictionary()['Track ID']).get_value()
... or:
id_strings = [PKey(PDict(item).dictionary()['Track ID']).get_value() for item in pods.get_array()]
# Show the first ten 'Track ID':
print(id_strings[:10])
    """
    # see also:
    #	https://github.com/dw/plistop/blob/master/plistop.py
    return astr.strip()


# Main script
if __name__ == "__main__":
    print("Please import me.")
