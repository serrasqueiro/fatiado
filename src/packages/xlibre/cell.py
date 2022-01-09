# (c)2021  Henrique Moreira

""" cell -- OpenLibre cell wrapper
"""

# pylint: disable=missing-function-docstring

import datetime


class CellFormat():
    """ Generic cell formating """
    _default_show_iso = True

    def __init__(self):
        self._show_iso = CellFormat._default_show_iso

    def set_default_iso(self, is_iso:True):
        self._default_show_iso = is_iso
        assert is_iso in (True, False)

    def show_iso_date(self) -> bool:
        return self._show_iso


class Textual(CellFormat):
    """ Textual cell """
    # pylint: disable=line-too-long

    def __init__(self, cell):
        # pylint: disable=line-too-long
        super().__init__()
        self._cell = cell
        self.value = None
        self.string = ""
        if cell is not None:
            self.string = self._from_cell(cell)
            #print(f"Textual(), empty?{self.string is None}, for {cell.column_letter}{cell.row}={self.string}")

    def empty(self) -> bool:
        return self._cell is None

    def cell(self):
        return self._cell

    def coordinate(self) -> str:
        """ Returns Excel coordinate of cell, e.g. B9 """
        return self._cell.coordinate

    def datatype(self) -> str:
        if self._cell is None:
            return ""
        return self._cell.data_type

    def __str__(self) -> str:
        return self.string

    def __repr__(self):
        if isinstance(self.value, (int, float)):
            return self.string
        if self.string is None:
            return 'null'
        return "'" + self.string + "'"

    def _from_cell(self, cell):
        value = cell.value
        datatype = cell.data_type
        if datatype == "d":	# date/ date and time
            if isinstance(value, datetime.time):
                t_format = "%H:%M:%S"
            else:
                t_format = "%Y-%m-%d" if self._show_iso else "%Y-%d-%m"
            try:
                text = value.strftime(t_format)
            except AttributeError:
                text = "?"
        elif datatype == "n":	# numeric
            text = None if value is None else str(value)
        else:
            text = value
        self.value = value
        return text


if __name__ == "__main__":
    print("Import me!")
