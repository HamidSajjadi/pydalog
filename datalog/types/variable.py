class Variable:
    __slots__ = ['name']

    def __init__(self, name: str):
        if not name:
            raise Exception('Provide a name for variable')
        self.name = name

    def __str__(self) -> str:
        return self.name
