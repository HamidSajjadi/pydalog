from __future__ import annotations

from typing import List, Iterable

from datalog.exceptions import RangeRuleError
from .built_in_literal import BuiltInLiteralAbstract
from .literal import Literal, Fact


class Rule:
    """
    parent(X,Y) <= father(X,Y)
    """
    __slots__ = ['_label', 'head', 'body', 'ground', '__head_variables', '__body_variables']

    def __init__(self, label: str, head: Literal, body: list):
        self._label = label

        if not isinstance(head, Literal):
            raise TypeError('Head should be a predicate')

        if not body or not len(body):
            raise TypeError(
                'you should add a predicate in rule body, if you want to define a rule with no body (aka fact), use a '
                'Fact object')

        bodies_as_literal = []
        for b in body:
            b_literal = b if isinstance(b, Literal) else Literal(b[0], *b[1:])
            bodies_as_literal.append(b_literal)

        self.head = head
        self.body: List[Literal] = bodies_as_literal

        self.__assert_range_of_rule()

    def substitute(self, bindings: dict) -> Rule:
        head_sub = self.head.substitute(bindings)
        body_sub = [b.substitute(bindings) for b in self.body]
        return Rule(label=self._label, head=head_sub, body=body_sub)

    def match_goals(self, facts: Iterable[Fact], goals: Iterable[Literal] = None, bindings: dict = None):
        if not goals:
            goals = self.body
        if not bindings:
            bindings = {}
        goal = goals[0]
        last_goal = len(goals) == 1
        answers = []
        if goal.is_builtin() or isinstance(goal, BuiltInLiteralAbstract):
            matched, new_bindings = goal.evaluate(bindings)
            if matched:
                if last_goal:
                    answers.append(new_bindings)
                else:
                    answers.extend(self.match_goals(facts, goals[1:], new_bindings))
        for fact in facts:
            matched, new_bindings = fact.unify(goal, bindings)
            if matched:
                if last_goal:
                    answers.append(new_bindings)
                else:
                    answers.extend(self.match_goals(facts, goals[1:], new_bindings))

        return answers

    def __assert_range_of_rule(self):
        """
        asserts that all variables in the head also appear in the body of rule
        :return:
        """
        head_variables = self.head.get_variables()
        body_variables = []
        body_variables.extend([b.get_variables for b in self.body])

        if len(head_variables) > len(body_variables):
            return RangeRuleError(self._label)

        for var in head_variables:
            if var not in body_variables:
                return RangeRuleError(self._label)

        # all elements were same.
        return True

    def __str__(self) -> str:
        return '{}: {} <== {}'.format(self._label, self.head, ', '.join([arg.__str__() for arg in self.body]))

    def __repr__(self):
        return self.__str__()
