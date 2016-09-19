# Provide "layout.dimensions".
CLASS Layout
    PART INIT
        self.c.provide("layout.dimensions", None, self.impl.dimensions)
        self.impl.dim = ["0", "0"]
    PART ASSIGN
        self.dim = [str(width),
                    str(height)]
    PART IMPL
        def dimensions(self, key):
            return self.dim
