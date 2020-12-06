from datalog import Datalog


def create_program() -> Datalog:
    return Datalog() \
        .add_fact('mother', 'sara', 'akbar') \
        .add_fact('mother', 'soghra', 'sara') \
        .add_fact('father', 'ahmad', 'akbar') \
        .add_rule(head=('parent', 'X', 'Y'), body=(('father', 'X', 'Y'),)) \
        .add_rule(head=('parent', 'X', 'Y'), body=(('mother', 'X', 'Y'),)) \
        .add_rule(head=('married', 'X', 'Y'), body=(('mother', 'X', 'Z'), ('father', 'Y', 'Z'))) \
        .add_rule(head=('married', 'Y', 'X'), body=(('married', 'X', 'Y'),)) \
        .add_rule(head=('descendant', 'X', 'Y'), body=(('parent', 'X', 'Y'),)) \
        .add_rule(head=('descendant', 'X', 'Y'), body=(('parent', 'X', 'Z'), ('parent', 'Z', 'Y')))


def run_extend_db():
    program = create_program()
    program.extend_db()
    print(program)


def run_query():
    program = create_program()
    print(program.query('descendant', 'X', 'akbar'))
    print(program.query('married', 'sara', 'ahmad'))
    print(program.query('married', 'sara', 'akbar'))


if __name__ == '__main__':
    # run_extend_db()
    run_query()
