# pydalog
Python implementation of a very basic, inefficient datalog


## Example
Creating a new datalog program
```python
from datalog import Datalog

program = Datalog() \
        .add_fact('mother', 'sara', 'akbar') \
        .add_fact('mother', 'soghra', 'sara') \
        .add_fact('father', 'ahmad', 'akbar') \
        .add_rule(head=('parent', 'X', 'Y'), body=(('father', 'X', 'Y'),)) \
        .add_rule(head=('parent', 'X', 'Y'), body=(('mother', 'X', 'Y'),)) \
        .add_rule(head=('married', 'X', 'Y'), body=(('mother', 'X', 'Z'), ('father', 'Y', 'Z'))) \
        .add_rule(head=('married', 'Y', 'X'), body=(('married', 'X', 'Y'),)) \
        .add_rule(head=('descendant', 'X', 'Y'), body=(('parent', 'X', 'Y'),)) \
        .add_rule(head=('descendant', 'X', 'Y'), body=(('parent', 'X', 'Z'), ('parent', 'Z', 'Y')))
```

Compile the program and fetch new rules using `extend_db()` function
```python
program.extend_db()
```

Query facts with `query(literal)` function. If the literal is a `Fact` (arguments are all constant and not variable) returns a boolean indicating whether this fact is true or not.

If literal is not a fact and has some variables, returns the binding that will make a correct fact from the given literal
```python
program.query('descendant', 'X', 'akbar') # returns [{X: 'sara'}, {X: 'ahmad'}, {X: 'soghra'}]
program.query('married', 'sara', 'ahmad') # returns True
program.query('married', 'sara', 'akbar') # returns False

```


look at run.py for example of a simple datalog program

