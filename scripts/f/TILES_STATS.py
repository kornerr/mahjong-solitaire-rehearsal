# Provide "tiles.stats".
CLASS Tiles
    PART INIT
        # Report only.
        self.c.provide("tiles.stats")
    PART IMPL
        def reportStats(self):
            tilesNb    = len(self.ids)
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
            # Report.
            val = [str(tilesNb),
                   "1" if hasMatches else "0"]
            self.c.report("tiles.stats", val)
    PART REFRESH
        self.reportStats()
