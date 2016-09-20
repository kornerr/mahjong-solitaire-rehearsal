# Provide 'tiles.refreshAvailability' and use it.
CLASS Main
    PART IMPL
        self.c.set("tiles.refreshAvailability", "1")
CLASS Tiles
    PART INIT
        self.c.provide("tiles.refreshAvailability",
                       self.impl.setRefreshAvailability)
    PART IMPL
        def setRefreshAvailability(self, key, value):
            print "setRefreshAvailability", key, value
