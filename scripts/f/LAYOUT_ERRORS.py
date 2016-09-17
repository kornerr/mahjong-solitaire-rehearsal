# Checks for layout errors.
CLASS Layout
    PART CONST
        LAYOUT_VERSIONS = ["1.0",
                           "1.1"]
    PART DEPTH
        if depth and len(fields) != depth:
            err = "Invalid field depth. Got/expected: '{0}/{1}'"
            self.errlist.append(err.format(len(fields),
                                           depth))
    PART IMPL
        def errors(self, key):
            return self.errlist
    PART INIT
        self.c.provide("layout.errors", None, self.impl.errors)
        self.impl.errlist = []
    PART RESET
        self.errlist = []
    PART VERSION
        if version not in LAYOUT_VERSIONS:
            self.errlist.append("Unsupported version: '{0}'".format(version))
