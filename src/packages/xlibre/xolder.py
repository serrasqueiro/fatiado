# (c)2022  Henrique Moreira

""" xolder -- Old Excel (xls) reader; hopefully you should not use this!
"""

# pylint: disable=missing-function-docstring

import xlrd


class ABook():
    """ Old Excel book content, wrapper """
    def __init__(self, name=""):
        self._aname = name
        self._workbook = None
        self.ibook = None

    def get_book_type(self):
        return "xls"

    def load(self, fname:str) -> bool:
        book = xlrd.open_workbook(fname)
        self._workbook = book
        self.ibook = OldBook(book, self._aname)
        return True

    def book(self):
        assert self._workbook is not None, self._aname
        return self._workbook


class OldBook():
    """ Old Excel book content, wrapper """
    def __init__(self, book=None, name=""):
        self._aname = name
        self._skel = book
        self.current = None	# Current sheet
        self._sheet_list = book._sheet_list

    def get_aname(self):
        return self._aname

    def first(self):
        return self._get_by_index(0)

    def goto_sheet(self, idx=0):
        return self._get_by_index(idx)

    def _get_by_index(self, idx:int):
        sht = self._skel.sheet_by_index(idx)
        position = sht._position
        self.current = OldSheet(sht, (self._skel, position, sht.name, sht.number))
        return sht


class OldSheet():
    """ Old xlrd excel Sheet """
    def __init__(self, sht, tup=None):
        self._sheet = sht
        self._skel = None
        self._lines = []
        if tup is None:
            self._original_sheet = None
        else:
            book, position, name, number = tup
            self._original_sheet = xlrd.sheet.Sheet(book, position, name, number)
        self._parse_lines()

    def content(self):
        return self._sheet

    def lines(self):
        return self._lines

    def _parse_lines(self):
        if self._sheet is None:
            return False
        res, lst = [], self._sheet._cell_values
        for line in lst:
            row = [better_content(ala) for ala in line]
            res.append(row)
        self._lines = res
        return True

def better_content(new):
    """ Returns slightly improved cell content. """
    #print(":::", type(new), new)
    try:
        astr = new.rstrip()
    except AttributeError:
        astr = new
    return astr


if __name__ == "__main__":
    print("Import me!")
