class PredicateInvalidException(Exception):

    def __init__(self, title: str, message: str):
        error_message = 'Error in predicate {}. {}'.format(title, message)
        super(PredicateInvalidException, self).__init__(error_message)


class RuleRangeError(Exception):
    def __init__(self, title: str):
        error_message = 'Error in rule {}. {}'.format(title,
                                                      'Every variable in rule head should appear in at least one of '
                                                      'the predicates in body')
        super(RuleRangeError, self).__init__(error_message)
