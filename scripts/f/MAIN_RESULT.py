# Detect game result.
CLASS Main
    PART INIT
        self.c.listen("tiles.stats", None, self.impl.onStats)
    PART IMPL
        def onStats(self, key, value):
            print "onStats", key, value
            hasTiles = int(value[0])
            hasMatches = int(value[1])
            print "has tiles/matches", hasTiles, hasMatches
            if (not hasTiles):
                print "Victory"
            elif (not hasMatches):
                print "Loss"
