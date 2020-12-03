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

        self._args = converted_args

    def get_variables(self) -> List[Variable]:
        return list(set([var for var in self._args if isinstance(var, Variable)]))

    def __str__(self) -> str:
        """
        returns predicate(arg1,arg2)
        :return:
        """
        return "{}({})".format(self.name,
                               ', '.join([arg.__str__() for arg in self._args]) if self._arity else '')
