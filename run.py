from datalog.types import Literal, Variable, Fact, Rule, Constant


def run():
    father_pred = Literal('father', [Variable('X'), Variable('Z'), '2', 2])
    print(father_pred)
    print([Variable('S')] == [Variable('S')])


if __name__ == '__main__':
    run()
