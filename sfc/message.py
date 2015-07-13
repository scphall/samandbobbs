from decorators import singleton

__all__ = ['msg']


@singleton
class Message(object):
    '''Message service
    Verbosity is vaguely:
        0 Silent
        1 Normal
        2 Verbose
    '''
    def __init__(self, verbosity=0):
        self._verbosity = verbosity
        self._default = 1
        return

    def __call__(self, arg, level=None):
        if isinstance(arg, int) and level is None:
            self._verbosity = arg
        else:
            self._print(arg, self._default if level is None else level)
        return

    def _print(self, msg, level):
        if level <= self._verbosity:
            print msg
        return


msg = Message()
