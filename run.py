from datalog.types import Predicate, Variable, Fact, Rule, Constant


def run():
    father_pred = Predicate('father', [Variable('X'), Variable('Z'), '2', 2])
    print(father_pred)


if __name__ == '__main__':
    run()
