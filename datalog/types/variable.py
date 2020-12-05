from __future__ import annotations

import re


class Variable:
    name: str

    def __init__(self, name: str):
        if not name:
            raise Exception('Provide a name for variable')

        if not Variable.is_variable(name):
            raise Exception('{} is invalid as a variable, it should start with capital letter'.format(name))

        self.name = name

    def equal(self, other: Variable):
        if not (other and isinstance(other, Variable)):
            return False
        return self.name == other.name

    def __to_string(self):
        return '{}'.format(self.name)

    def __repr__(self):
        return self.__to_string()

    def __str__(self) -> str:
        return self.__to_string()

    def __eq__(self, other: Variable):
        return self.equal(other)

    def __hash__(self):
        return hash('Variable' + self.__to_string())

    @staticmethod
    def is_variable(var):
        if isinstance(var, Variable):
            return True
        if isinstance(var, str) and re.match(r"\b[A-Z].*?\b", var):
            return True
        return False
