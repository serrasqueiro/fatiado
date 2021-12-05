#-*- coding: utf-8 -*-
# genarray.py  (c)2021  Henrique Moreira

"""
generic plist
"""

# pylint: disable=missing-function-docstring


class PList():
    """ Abstract PList class """
    def __init__(self, tag: str):
        self._tag = tag
        self._array = []

    def get_tag(self) -> str:
        """ Returns this element's tag """
        assert self._tag
        return self._tag

    def get_array(self) -> list:
        return self._array

    def first_array(self) -> list:
        """ Returns the array within the dictionary
        """
        if not self._array:
            return self._array
        assert len(self._array) == 1, "One array per element!"
        return self._array[0]


class PDict(PList):
    """ plist 'dict'
    """
    def __init__(self, elem):
        super().__init__(elem.tag)
        self._dict = {}
        is_ok = self._parse(elem)
        assert is_ok

    def dictionary(self) -> dict:
        """ Returns the dictionary
        """
        return self._dict

    def element_by_key(self, key: str):
        """ Returns the raw element by key name
        """
        return self._dict[key]

    def str_by_key(self, key: str):
        """ Returns the associated string """
        return self._dict[key].getnext().text

    def _parse(self, elem) -> bool:
        """ Parses a dictionary-like element """
        assert elem.tag == "dict"
        for item in elem.findall("./key"):
            self._dict[item.text] = item
        for item in elem.findall("./array"):
            self._array.append(item)
        return True


class PArray(PList):
    """ plist 'array'
    """
    def __init__(self, elem):
        super().__init__(elem.tag)
        self._dict = {}
        is_ok = self._parse(elem)
        assert is_ok

    def _parse(self, elem) -> bool:
        """ Parses a array-like element """
        assert elem.tag == "array"
        for item in elem:
            self._array.append(item)
        return True


class PKey(PList):
    """ plist 'key'
    """
    def __init__(self, elem):
        super().__init__(elem.tag)
        self._value = ""
        is_ok = self._parse(elem)
        assert is_ok

    def get_value(self):
        return self._value

    def _parse(self, elem) -> bool:
        """ Parses a key-like element """
        assert elem.tag == "key"
        anext = elem.getnext()
        avalue = anext.text
        self._value = avalue
        return True


# Main script
if __name__ == "__main__":
    print("Please import me.")
