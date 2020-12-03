from .predicate import Predicate
from datalog.exceptions import RuleRangeError


class Rule:
    """
    parent(X,Y) <= father(X,Y)
    """
    __slots__ = ['_label', 'head', 'body', 'ground', '__head_variables', '__body_variables']

    def __init__(self, label: str, head: Predicate, body: list):
        self._label = label

        if not isinstance(head, Predicate):
            raise TypeError('Head should be a predicate')

        if not body or not len(body):
            raise TypeError(
                'you should add a predicate in rule body, if you want to define a rule with no body (aka fact), use a '
                'Fact object')

        self.head = head
        self.body = body

        self.__assert_range_of_rule()

    def __assert_range_of_rule(self):
        """
        asserts that all variables in the head also appear in the body of rule
        :return:
        """
        head_variables = self.head.get_variables()
        body_variables = []
        body_variables.extend([b.get_variables for b in self.body])

        if len(head_variables) > len(body_variables):
            return RuleRangeError(self._label)

        for var in head_variables:
            if var not in body_variables:
                return RuleRangeError(self._label)

        # all elements were same.
        return True

    def __str__(self) -> str:
        return '{}: {} <== {}'.format(self._label, self.head, ', '.join([arg.__str__() for arg in self.body]))
