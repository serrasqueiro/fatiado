# (c)2022  Henrique Moreira

""" lesser -- part of OpenLibre wrapper: less information, but serializable
"""

# pylint: disable=missing-function-docstring

import json
from xlibre.cell import Textual


class Contx():
    """ Serializable sheet content """
    def __init__(self, sht=None, desc="", start_content_row=1):
        self._sheet = sht
        self._description = desc
        self._start_row = int(start_content_row)
        self.rows = []
        self.parse()

    def start_row(self) -> int:
        return self._start_row

    def max_row(self) -> int:
        return self._sheet.max_row

    def max_column(self) -> int:
        return self._sheet.max_column

    def parse(self) -> bool:
        if self._sheet is None:
            return False
        idx = 0
        self._init_parse()
        for row in self._sheet.rows:
            idx += 1
            if idx < self._start_row:
                continue
            alist = [Simplex(item.value, item.data_type) for item in row]
            self.rows.append(alist)
        return True

    def _init_parse(self):
        self.rows = []

    def to_json(self) -> str:
        data = []
        for row in self.rows:
            elem = [None if elem.is_null() else str(elem) for elem in row]
            data.append(elem)
        astr = json.dumps(data, sort_keys=True, ensure_ascii=False, indent=2)
        return astr


class Simplex(list):
    """ Simpler class """
    default_null = "<null>"

    def __init__(self, value, data_type="s"):
        assert isinstance(data_type, str)
        dttp = data_type
        devalue = 0
        if dttp == "n":
            cell = ""
            devalue = -1
        elif dttp == "s":
            cell = value
        else:
            cell = data_type + "?"
        self._inner = [cell, devalue]

    def __getitem__(self, index):
        return self._inner.__getitem__(index)

    def __setitem__(self, index, value):
        return self._inner.__setitem__(index, value)

    def __str__(self):
        _, devalue = self._inner
        if devalue == -1:
            return Simplex.default_null
        return self._inner[0]

    def __repr__(self):
        return "'" + self._inner[0] + "'"

    def is_null(self):
        return self._inner[1] == -1

    def append(self, value):
        self.insert(len(self) + 1, value)

if __name__ == "__main__":
    print("Import me!")
