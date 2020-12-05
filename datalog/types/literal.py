from __future__ import annotations

from typing import List, Union, Dict

from .constant import Constant
from .predicate import Predicate
from .variable import Variable


class Literal(Predicate):
    __slots__ = ["args"]

    def __init__(self, predicate: Union[Predicate, str], *args):

        arity = 0 if not args else len(args)
        if isinstance(predicate, Predicate):
            if predicate.arity != arity:
                raise IndexError(
                    'predicate {} arity is {}, you provided {} arguments'.format(predicate, predicate.arity, arity))
            name = predicate.name
        else:
            name = predicate

        super().__init__(name, arity)
        self.__set_args(args)

    def __set_args(self, args: tuple):

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
        self.args = tuple(converted_args)

    def predicate(self) -> Predicate:
        return Predicate(self.name, self.arity)

    def substitute(self, bindings: dict):
        new_args = [bindings[arg] if arg in bindings.keys() else arg for arg in self.args]
        return Literal(self.predicate(), *new_args)

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
        return self.__to_string().__hash__()

    def __lt__(self, other: Literal):
        return self.__to_string().__lt__(other.__str__())

    @staticmethod
    def get_binding(literal: Literal, fact: Fact) -> dict:
        if literal.predicate() != fact.predicate():
            raise Exception('fact and literal are not of the same predicate')
        binding = {}
        for i, _ in enumerate(literal.args):
            binding[literal.args[i]] = fact.args[i]
        return binding


class Fact(Literal):

    def match(self, literal: Literal, original_bindings=None):
        bindings: Dict[Variable, str] = {}
        if original_bindings:
            for key, value in original_bindings.items():
                bindings[Variable(key)] = value

        if literal.predicate() != self.predicate():
            return False

        for i, var in enumerate(literal.args):
            if Variable.is_variable(var):
                if var in bindings and bindings[var] != self.args[i]:
                    return False
                bindings[var] = self.args[i]
        return bindings

    def __init__(self, name: Union[Predicate, str], *args):

        for arg in args:
            if Variable.is_variable(arg):
                raise TypeError('fact can not have variable')

        super().__init__(name, *args)
