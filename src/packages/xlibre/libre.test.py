# (c)2021  Henrique Moreira

""" libre.test.py -- libre.py module tester
"""

# pylint: disable=missing-function-docstring

import sys
from xlibre.libre import Book


def main():
    run_test(sys.argv[1:])


def run_test(paths:list):
    assert paths, "At least one xlsx file!"
    for path in paths:
        run_book_test(path)


def run_book_test(path:str):
    wbk = Book(path)
    till_row = 1	# use 2 or n...when xlsx has more than one line heading
    is_ok = wbk.parse_headings(1, till_row)
    assert is_ok
    sht_idx = 1
    heads = wbk.headings[sht_idx]
    cols = heads.columns()
    assert cols
    print(cols)
    print("=" * 20)
    print(heads.by_column())
    print("=" * 20)
    print(heads.get_columns("by-name"))
    wbk.parse(1)	# parse the first sheet
    print(">>>" * 20)
    rows = wbk.contents[1].rows
    idx = 0
    for row in rows:
        print("row#", idx+wbk.contents[1].start_row(), end=": ")
        print(row)
        idx += 1
    print("<<<" * 20)


if __name__ == "__main__":
    main()
