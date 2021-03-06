from __future__ import annotations

from .variable import Variable


class Constant:
    __slots__ = ['value']

    def __init__(self, value):
        if not value:
            raise Exception('Provide a value for constant')
        self.value = value

    def equal(self, other: Constant):
        if not other:
            return False
        if Variable.is_variable(other):
            return False
        if not isinstance(other, Constant):
            return self.value == other
        
        return self.value == other.value

    def __to_string(self):
        return self.value.__repr__()

    def __eq__(self, other):
        return self.equal(other)

    def __hash__(self):
        return ('constant' + self.__to_string()).__hash__()

    def __repr__(self):
        return self.__to_string()

    def __str__(self) -> str:
        return self.__to_string()
