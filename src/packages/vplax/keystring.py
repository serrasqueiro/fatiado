# (c)2021  Henrique Moreira

""" keystring -- simplified strings with keys

CUE files have 'QUOTED_STR KEY' or 'KEY QUOTED_STR'
This module helps both cases.
"""

# pylint: disable=missing-function-docstring

class KeyString():
    """ KeyString basic class """
    def __init__(self, astr:str="", separator:str=" "):
        self._string = astr
        self.strings = self._decouple(astr, separator)

    def _decouple(self, astr, asep) -> list:
        """ Parses string and decouples quotes where necessary """
        #	REM COMMENT "ExactAudioCopy v..."
        # or
        #	FILE "abc def.flac" WAVE
        idx = 0
        last, items = "", []
        lastchar = ""
        while idx < len(astr):
            achr = astr[idx]
            idx += 1
            if achr == '"':
                if last:
                    items.append(last)
                    if asep:
                        items.append(None)
                    last = ""
                pos = astr[idx:].find('"')
                if pos >= 0:
                    items.append(astr[idx:idx+pos])
                    idx += pos + 1
                    continue
            if achr == asep:
                items.append(last)
                last = ""
                continue
            last += achr
        if last:
            items.append(last)
        return items


if __name__ == "__main__":
    print("Import me!")
