from abc import ABC, abstractmethod
from typing import Tuple

from .literal import Literal
from .variable import Variable


class BuiltInLiteralAbstract(ABC, Literal):

    @abstractmethod
    def evaluate(self, bindings: dict = None) -> Tuple[bool, dict]:
        pass

    def is_builtin(self):
        return True

    def _check_args_bound(self, bindings, convert_to_float=False):
        term1 = self.args[0]

        if Variable.is_variable(term1) and term1 in bindings:
            term1 = bindings[term1]

        term2 = self.args[1]
        if Variable.is_variable(term2) and term2 in bindings:
            term2 = bindings[term2]

        if Variable.is_variable(term1) or Variable.is_variable(term2):
            raise AttributeError('both values are unbound for {} predicate'.format(self.predicate()))

        if convert_to_float:
            term1 = float(term1.value)
            term2 = float(term2.value)
        return term1, term2


class Eq(BuiltInLiteralAbstract):
    name = 'eq'

    def __init__(self, arg1, arg2):
        super().__init__(self.name, arg1, arg2)

    def substitute(self, bindings: dict):
        new_args = [bindings[arg] if arg in bindings.keys() else arg for arg in self.args]
        return Literal(self.predicate(), *new_args)

    def evaluate(self, bindings: dict = None) -> Tuple[bool, dict]:
        if not bindings:
            bindings = {}
        term1 = self.args[0]
        if Variable.is_variable(term1) and term1 in bindings:
            term1 = bindings[term1]

        term2 = self.args[1]
        if Variable.is_variable(term2) and term2 in bindings:
            term2 = bindings[term2]

        if Variable.is_variable(term1) and Variable.is_variable(term2):
            raise AttributeError('both values are unbound for Eq predicate')

        if Variable.is_variable(term1):
            bindings[term1] = term2
            return True, bindings
        elif Variable.is_variable(term2):
            bindings[term2] = term1
            return True, bindings
        else:
            match = term1 == term2
            return match, bindings


class Lt(BuiltInLiteralAbstract):
    name = 'lt'

    def __init__(self, arg1, arg2):
        super().__init__(self.name, arg1, arg2)

    def evaluate(self, bindings: dict = None) -> Tuple[bool, dict]:
        try:
            (term1, term2) = self._check_args_bound(bindings, convert_to_float=True)
            return term1 < term2, bindings
        except ValueError:
            return False, bindings


class Lte(BuiltInLiteralAbstract):
    name = 'lte'

    def __init__(self, arg1, arg2):
        super().__init__(self.name, arg1, arg2)

    def evaluate(self, bindings: dict = None) -> Tuple[bool, dict]:

        try:
            (term1, term2) = self._check_args_bound(bindings, convert_to_float=True)
            return term1 <= term2, bindings
        except ValueError:
            return False, bindings


class Gt(BuiltInLiteralAbstract):
    name = 'gt'

    def __init__(self, arg1, arg2):
        super().__init__(self.name, arg1, arg2)

    def evaluate(self, bindings: dict = None) -> Tuple[bool, dict]:
        try:
            (term1, term2) = self._check_args_bound(bindings, convert_to_float=True)
            return term1 > term2, bindings
        except ValueError:
            return False, bindings


class Gte(BuiltInLiteralAbstract):
    name = 'gte'

    def __init__(self, arg1, arg2):
        super().__init__(self.name, arg1, arg2)

    def evaluate(self, bindings: dict = None) -> Tuple[bool, dict]:
        try:
            (term1, term2) = self._check_args_bound(bindings, convert_to_float=True)
            return term1 >= term2, bindings
        except ValueError:
            return False, bindings


class Neq(BuiltInLiteralAbstract):
    name = 'neq'

    def __init__(self, arg1, arg2):
        super().__init__(self.name, arg1, arg2)

    def evaluate(self, bindings: dict = None) -> Tuple[bool, dict]:
        (term1, term2) = self._check_args_bound(bindings, convert_to_float=False)
        return term1 != term2, bindings
