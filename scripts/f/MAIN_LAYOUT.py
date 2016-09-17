# Load provided layout.
CLASS Main
    PART CONST
        MAIN_LAYOUT     = "X_shaped"
        #MAIN_LAYOUT     = "cat"
        #MAIN_LAYOUT     = "default"
        MAIN_LAYOUT_DIR = "layouts"
        MAIN_LAYOUT_EXT = "layout"
        MAIN_RESOLVER   = "pathResolver.MainResolver"
    PART INIT
        self.c.setConst("RESOLVER", MAIN_RESOLVER)
    PART IMPL
        fileName = "{0}/{1}.{2}".format(MAIN_LAYOUT_DIR,
                                        MAIN_LAYOUT,
                                        MAIN_LAYOUT_EXT)
        self.c.set("$RESOLVER.resolveFileNameAbs", fileName)
        fileNameAbs = self.c.get("$RESOLVER.fileNameAbs")
        self.c.set("layout.parseFileName", fileNameAbs)
        print "errors", self.c.get("layout.errors")
        print "positions", self.c.get("layout.positions")
