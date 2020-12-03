import unittest
from datalog.types import Predicate, Variable


class TestPredicate(unittest.TestCase):

    def test_init(self):
        pred_name = 'father'
        args = [Variable('X'), Variable('Z'), 'a']
        pred = Predicate(pred_name, args)
        self.assertIsInstance(pred, Predicate)
        self.assertEqual(pred.name, pred_name)
        self.assertEqual(pred.arity(), len(args))
        self.assertEqual(args, pred.args())
        self.assertIsInstance()

    def test_equality(self):
        pred_name = 'father'
        args1 = [Variable('X'), Variable('Z')]
        args2 = [Variable('X'), 'Z']
        first_pred = Predicate(pred_name, args1)
        second_pred = Predicate(pred_name, args1)

        self.assertTrue(first_pred == second_pred, 'expected {} and {} to be equal'.format(first_pred, second_pred))

        different_arity_pred = Predicate(pred_name, args1 + args1)

        self.assertFalse(first_pred == different_arity_pred,
                         '__eq__ should return false for predicate with different arities, ({} != {})'.format(
                             first_pred, different_arity_pred))

        different_pred = Predicate(pred_name, args2)
        self.assertFalse(first_pred == different_pred,
                         'expected {} and {} to not be equal'.format(first_pred, different_pred))


if __name__ == '__main__':
    unittest.main()
