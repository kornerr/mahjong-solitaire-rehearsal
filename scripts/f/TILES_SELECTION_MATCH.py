# Provide "tiles.match" and "matchSuccess" sequence.
CLASS Tiles
    PART CONST
        TILE_MATCH_API              = "tiles.match"
        TILE_SEQUENCE_MATCH_SUCCESS = "sequence.default.matchSuccess"
    PART INIT
        self.c.setConst("SEQMATCH", TILE_SEQUENCE_MATCH_SUCCESS)
        self.c.provide(TILE_MATCH_API, self.setMatch)
        self.lastMatchedTile = None
    PART IMPL
        def setMatch(self, key, value):
            # Try to match.
            if (self.lastMatchedTile):
                id1 = self.ids[self.lastMatchedTile]
                id2 = self.ids[self.lastSelectedTile]
                # Successful match.
                if (id1 == id2):
                    print "match!"
                    self.c.set("$SEQMATCH.active", "1")
            self.lastMatchedTile = self.lastSelectedTile
            self.c.report(TILE_MATCH_API, "0")
    PART DELETE
        if (self.lastMatchedTile and
            (self.lastMatchedTile == tileName)):
            self.lastMatchedTile = None
