# (c)2021  Henrique Moreira

""" cell -- OpenLibre cell wrapper
"""

# pylint: disable=missing-function-docstring

import datetime


class Textual():
    """ Textual cell """
    def __init__(self, cell):
        self._cell = cell
        self.value = None
        self.string = ""
        if cell is not None:
            self.string = self._from_cell(cell)

    def empty(self) -> bool:
        return self._cell is None

    def datatype(self) -> str:
        if self._cell is None:
            return ""
        return self._cell.data_type

    def __str__(self) -> str:
        return self.string

    def __repr__(self):
        if isinstance(self.value, (int, float)):
            return self.string
        return "'" + self.string + "'"

    def _from_cell(self, cell):
        value = cell.value
        datatype = cell.data_type
        if datatype == "d":	# date/ date and time
            if isinstance(value, datetime.time):
                t_format = "%H:%M:%S"
            else:
                t_format = "%Y-%d-%m"
            try:
                text = value.strftime(t_format)
            except AttributeError:
                text = "?"
        elif datatype == "n":	# numeric
            text = str(value)
        else:
            text = value
        self.value = value
        return text


if __name__ == "__main__":
    print("Import me!")
