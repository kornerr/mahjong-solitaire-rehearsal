# Detect game result.
# Provide "main.checkResult", "tiles.stats".
CLASS Main
    PART CONST
        MAIN_RESULT_API = "main.checkResult"
    PART INIT
        self.c.provide(MAIN_RESULT_API, self.setCheckResult)
    PART IMPL
        def setCheckResult(self, key, value):
            (hasTiles, hasMatches) = self.c.get("tiles.stats")
            if (hasTiles == "0"):
                print "Victory"
            elif (hasMatches == "0"):
                print "Loss"
            self.c.report(MAIN_RESULT_API, "0")
CLASS Tiles
    PART CONST
        TILES_STATS_API = "tiles.stats"
    PART INIT
        self.c.provide(TILES_STATS_API, None, self.stats)
    PART IMPL
        def stats(self, key):
            hasTiles   = len(self.ids) > 0
            hasMatches = False
            # Find out if there is at least one pair
            # of matching tiles available.
            ids = { }
            for tileName in self.available:
                id = self.ids[tileName]
                if (id not in ids):
                    ids[id] = 0
                ids[id] = ids[id] + 1
                # A pair has been found.
                if (ids[id] > 1):
                    hasMatches = True
                    break
            return ["1" if hasTiles else "0",
                    "1" if hasMatches else "0"]
