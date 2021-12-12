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

    def original_string(self) -> str:
        """ Returns the original string """
        return self._string

    def lean(self) -> list:
        """ Lean list """
        return [astr for astr in self.strings if astr is not None]

    def is_lean(self) -> bool:
        """ Returns True if there are no 'None' attributes in strings
        E.g. 'abc "def""ghi" xyz', yields:
		['abc', 'def', None, 'ghi', 'xyz']
        which is said to be 'not lean' !
        This function returns False in that case.
        """
        return len(self.strings) == len(self.lean())

    def _decouple(self, astr, asep) -> list:
        """ Parses string and decouples quotes where necessary """
        #	REM COMMENT "ExactAudioCopy v..."
        # or
        #	FILE "abc def.flac" WAVE
        idx = 0
        last, items = "", []
        achr = ""
        while idx < len(astr):
            lastchar = achr
            achr = astr[idx]
            idx += 1
            if achr == '"':
                if last:
                    items.append(last)
                    if asep:
                        items.append(None)
                    last = ""
                elif asep:
                    if lastchar == "QUOTE":
                        items.append(None)
                pos = astr[idx:].find('"')
                if pos >= 0:
                    items.append(astr[idx:idx+pos])
                    idx += pos + 1
                    achr = "QUOTE"
                continue
            if achr == asep:
                if lastchar == 'QUOTE' and not last:
                    pass
                else:
                    items.append(last)
                last = ""
                continue
            last += achr
        if last:
            items.append(last)
        return items


if __name__ == "__main__":
    print("Import me!")
