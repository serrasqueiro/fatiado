# (c)2021  Henrique Moreira

""" fileio -- text file reader/ writer
"""

# pylint: disable=missing-function-docstring

import os


class FileIO():
    """ Textual fileio """
    def __init__(self, path:str, encoding:str="utf-8", reader:bool=True):
        self._path, self._encoding = path, encoding
        if reader:
            self._data = open(path, "r", encoding="utf-8").read()
        else:
            self._data = ""

    def new_path(self, path:str):
        assert path
        assert isinstance(path, str)
        self._path = path

    def encoding(self) -> str:
        """ Returns the encoding (input). """
        return self._encoding

    def as_string(self) -> str:
        """ Return the content string. """
        return self._data

    def write(self, encoding:str="utf-8", content=None) -> int:
        data = self._data if content is None else content
        with open(self._path, "w", encoding=encoding) as fdout:
            try:
                res = fdout.write(data)
            except UnicodeEncodeError:
                res = -1
        # 'res' is the number of octets written
        return res

    def write_all(self, encoding:str="utf-8", content=None) -> bool:
        data = self._data if content is None else content
        to_write = len(data)
        written = self.write(encoding, data)
        return to_write == written

    def backup(self, encoding:str="utf-8", content=None, back_ext:str=".bak", remove=True) -> bool:
        """ Same as write, but saves an alternate file backup. """
        path = self._path
        assert path
        assert isinstance(back_ext, str)
        if not back_ext:
            return self.write(encoding, content)
        bkp_name = (path + "~") if path.endswith(back_ext) else (path + back_ext)
        with open(bkp_name, "w", encoding=self._encoding) as fdsafe:
            fdsafe.write(self._data)
        res = self.write(encoding, content)
        if res < 0:
            # Try to recover original file
            with open(path, "wb") as fdout:
                fdout.write(bytes(self._data, self._encoding))
            return False
        # Delete backup if needed...
        if remove:
            os.remove(bkp_name)
        return True


if __name__ == "__main__":
    print("Import me!")
