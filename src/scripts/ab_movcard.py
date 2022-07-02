#-*- coding: utf-8 -*-
# ab_movcard.py  (c)2021  Henrique Moreira

""" Dumps Excel movCard<N>-YYYYMMDD-HHMMSS.xlsx
"""

# pylint: disable=missing-docstring

import sys
from xlibre.libre import Book

def main():
    """ Main function """
    code = run(sys.argv[1:])
    if code is None:
        print(f"""Usage:

{__file__} movcard-xxx.xlsx
""")
    sys.exit(code if code else 0)

def run(args:list):
    """ Main script """
    param = args
    if not param:
        param = ["movcard.xlsx"]
    if param[0].startswith("-"):
        return None
    code, _ = go_cards(param)
    return code

def go_cards(param) -> tuple:
    """ Get info from Excel movement file(s)
    Example:
	code, alist = ab_movcard.go_cards(["movCardX-20220702-095740.xlsx"])
    """
    res = []
    for fname in param:
        comp = do_card(fname)
        res.append(comp)
    return 0, res

def do_card(fname:str):
    res = []
    wbk = Book(fname)
    wbk.parse_headings(1, 7)
    assert wbk.sheet_names()
    sh_name = wbk.sheet_names()[0]
    print("Sheet name:", sh_name)
    head = wbk.headings[-1]
    # Match columns
    cols = [asciied(cont[-1]) for _, cont in head.columns()]
    print(cols)
    wbk.parse()
    there = wbk.contents[1]
    #cont = [ala for ala in there.rows]
    cont = there.rows
    for idx, line in enumerate(cont, 1):
        aline = [cell.string.strip() for cell in line]
        avalue = line[3]
        euros = avalue.value
        movline = aline[:-1]
        res.append((idx, avalue.value, movline))
        print(f"{idx:4} {euros:>9.2f}", movline)
    return res

def asciied(astr):
    mapa = {
        0xe7: "c",	# c cedil
        0xe3: "a",	# a tilde
    }
    def valid(achr):
        demap = mapa.get(ord(achr))
        if demap is not None:
            return demap
        return achr if ' ' <= achr < '~' else ""

    if isinstance(astr, list):
        return [asciied(item) for item in astr]
    if hasattr(astr, "string"):
        return asciied(astr.string)
    assert isinstance(astr, str), f"Uops ({type(astr)}): {astr}"
    #	print([f"0x{ord(achr):02x}={achr}" for achr in astr])
    return ''.join([valid(achr) for achr in astr if valid(achr)])


if __name__=="__main__":
    main()
