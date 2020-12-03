import unittest
from datalog.types import Literal, Variable, Constant


class TestPredicate(unittest.TestCase):

    def test_init(self):
        pred_name = 'father'
        args = [Variable('X'), Variable('Z'), Constant('a')]
        pred = Literal(pred_name, args)
        self.assertIsInstance(pred, Literal)
        self.assertEqual(pred.name, pred_name)
        self.assertEqual(pred.arity(), len(args))
        self.assertEqual(args, pred.args())

    def test_equality(self):
        pred_name = 'father'
        args1 = [Variable('X'), Variable('Z')]
        args2 = [Variable('X'), 'Z']
        first_pred = Literal(pred_name, args1)
        second_pred = Literal(pred_name, args1)

        self.assertEqual(first_pred, second_pred, 'expected {} and {} to be equal'.format(first_pred, second_pred))

        different_arity_pred = Literal(pred_name, args1 + args1)

        self.assertFalse(first_pred == different_arity_pred,
                         '__eq__ should return false for predicate with different arities, ({} != {})'.format(
                             first_pred, different_arity_pred))

        different_pred = Literal(pred_name, args2)
        self.assertFalse(first_pred == different_pred,
                         'expected {} and {} to not be equal'.format(first_pred, different_pred))


if __name__ == '__main__':
    unittest.main()
