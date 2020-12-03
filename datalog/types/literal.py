from __future__ import annotations

from typing import List, Iterable, Set, Union

from .constant import Constant
from .variable import Variable
from .predicate import Predicate


class Literal(Predicate):
    __slots__ = ["args"]

    def __init__(self, predicate: Predicate = None, name: str = None, args: list = None):
        if not predicate and not name:
            raise AttributeError('provide either a name or a predicate object')

        arity = 0 if not args else len(args)
        if predicate:
            if predicate.arity != arity:
                raise IndexError(
                    'predicate {} arity is {}, you provided {} arguments'.format(predicate, predicate.arity, arity))
            name = predicate.name

        super().__init__(name, arity)
        self.__set_args(args)

    def __set_args(self, args: list):

        if not args:
            self.args = []
            return

        converted_args = []
        for arg in args:
            if isinstance(arg, Variable) or isinstance(arg, Constant):
                converted_args.append(arg)
            else:
                if Variable.is_variable(arg):
                    converted_args.append(Variable(arg))
                else:
                    converted_args.append(Constant(arg))
        self.args = converted_args

    def predicate(self) -> Predicate:
        return Predicate(self.name, self.arity)

    def get_variables(self) -> List[Variable]:
        return [var for var in self.args if isinstance(var, Variable)]

    def equal(self, other: Literal) -> bool:

        if not other or not isinstance(other, Literal):
            return False

        if other.name != self.name:
            return False

        if other.arity != self.arity:
            return False

        for i, _ in enumerate(self.args):
            if self.args[i] != other.args[i]:
                return False

        return True

    def __to_string(self):
        return "{}({})".format(self.name,
                               ', '.join([arg.__str__() for arg in self.args]) if self.arity else '')

    def __eq__(self, other: Literal):
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
