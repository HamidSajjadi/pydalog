from __future__ import annotations

from typing import List, Iterable, Set

from .constant import Constant
from .variable import Variable


class Predicate:
    __slots__ = ["name", "_arity", "_args"]

    def __init__(self, name: str, args: list = None):
        self.name = name
        self._arity = 0 if not args else len(args)

        converted_args = []
        for arg in args:
            if isinstance(arg, Variable):
                converted_args.append(arg)
            else:
                converted_args.append(Constant(arg))
        print(converted_args)
        self._args = converted_args

    def arity(self):
        return self._arity

    def args(self):
        return self._args

    def get_variables(self) -> List[Variable]:
        return [var for var in self._args if isinstance(var, Variable)]

    def equal(self, other: Predicate) -> bool:

        if not other or not isinstance(other, Predicate):
            return False

        if other.name != self.name:
            return False

        if other._arity != self._arity:
            return False

        for i, _ in enumerate(self._args):
            if self._args[i] != other._args[i]:
                return False

        return True

    def __to_string(self):
        return "{}({})".format(self.name,
                               ', '.join([arg.__str__() for arg in self._args]) if self._arity else '')

    def __eq__(self, other):
        """Overrides the default implementation"""
        return self.equal(other)

    def __str__(self) -> str:
        """
        returns predicate(arg1,arg2)
        :return:
        """
        return self.__to_string()

    def __repr__(self):
        return self.__to_string()

    def __hash__(self):
        return self.__to_string()
