#-*- coding: utf-8 -*-
# tuneinfo.py  (c)2021  Henrique Moreira

"""
itunes xml parser
"""

from lxml import etree  # type:ignore # nosec

# pylint: disable=missing-function-docstring

ITS_DESC = {
    "Major Version": (1, "major"),
    "Minor Version": (1, "minor"),
    "Application Version": ("12.x", "app-version"),
    "Date": ("%T@", "date"),
    "Features": (5, "features"),
    "Show Content Ratings": (True, "show-ratings"),
    "Library Persistent ID": ("?", "pers-id"),
    "Tracks": ("@dict", "tracks"),	# big!
    "Playlists": ("@dict", "playlists"),	# bigger!
    "Music Folder": ("/", "folder"),
}


class AbstractXML():
    """ Abstract/ generic XML class - reader """
    def __init__(self, data: str=""):
        self._lines = data.splitlines()
        self._root = self._set_root(data)

    def xml(self):
        """ Returns the root element """
        return self._root

    def _set_root(self, data: str):
        pos = data.find("\n")
        if data.startswith("<?xml") and pos > 0:
            head = data[:pos]
            if "encoding=" in head:
                data = data[pos:]
        root = etree.XML(data)
        return root


class TunesXML(AbstractXML):
    """ itunes XML parser """
    # pylint: disable=no-self-use

    def __init__(self, fname: str="", data: str=""):
        if fname:
            assert not data
            self._init_tunes(fname)
        else:
            super().__init__(data)
        self._parse()

    def _init_tunes(self, fname: str):
        with open(fname, "r", encoding="UTF-8") as fdin:
            data = fdin.read()
        super().__init__(data)

    def _parse(self):
        """ Iterate through iTunes keying """
        plist = self._root[0]
        its = self._convert_its_desc()
        blocks = {}
        for ala in plist.findall("./key"):
            is_ok = ala.tag == "key"
            assert is_ok, f"Wrong tag: '{ala.tag}' ({ala.text})"
            s_key, sample_str, _ = its.get(ala.text)
            assert s_key, f"Uops: {ala.text}"
            blocks[s_key] = ala
            big = sample_str[0] == "@"
            avalue = "<...>" if big else strvalue_from_element(ala)
            print(":::", s_key, "SAMPLE:", sample_str, big, "; value:", avalue)
        self._blocks = blocks
        return blocks

    def _convert_its_desc(self) -> dict:
        """ Converts itunes basic descriptors into a dictionary """
        res = {}
        for key, tup in ITS_DESC.items():
            sample, s_key = tup
            msg = f"Bogus sample: {sample}"
            assert isinstance(sample, (str, int, bool)), msg
            sample_str = from_its_sample(sample)
            res[key] = (s_key, sample_str, sample)
        return res


def strvalue_from_element(elem):
    """ Returns the value of a XML element as string
    """
    # f"{ala.getnext().text}={ala.getnext().tag}"
    there = elem.getnext()
    if there.tag in ("false", "true"):
        assert there.text is None
        return there.tag
    return there.text


def from_its_sample(value) -> str:
    """ Converts 'value', which can be str|int|bool
    into a reasonable string sequence.
    """
    if isinstance(value, bool):
        return "T" if value else "F"
    if isinstance(value, int):
        return f"{value}"
    if not isinstance(value, str):
        return ""
    return value


# Main script
if __name__ == "__main__":
    print("Please import me.")
