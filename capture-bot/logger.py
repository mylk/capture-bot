class Logger:
    verbose = False

    def __init__(self, verbose = False):
        self.verbose = verbose

    def write_console(self, message):
        if self.verbose:
            print message