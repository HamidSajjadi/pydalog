from datalog.types import Predicate, Variable, Fact, Rule


def run():
    father_pred = Predicate('father', ['X', 'Z'])
    fact = Fact(father_pred, ['Hossein', 'Hamid'])
    parent = Predicate('parent', [Variable('X'), Variable('Y')])
    rule = Rule('r1', parent, [father_pred])
    print(father_pred)
    print(fact)
    print(parent)
    print(rule)


if __name__ == '__main__':
    run()
