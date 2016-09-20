# Provide 'tile..id' and use it.
CLASS Main
    PART IMPL
        for p in positions:
            self.c.setConst("TILE", p)
            # Generate random number in [1; 9] range.
            id = rand() % 9 + 1
            self.c.set("tile.$TILE.id", str(id))
CLASS Tiles
    PART INIT
        self.c.provide("tile..id", self.impl.setTileID, self.impl.tileID)
        self.impl.ids = {}
    PART IMPL
        def tileID(self, key):
            tileName = key[1]
            if (tileName in self.ids):
                id = self.ids[tileName]
                return [str(id)]
            # Invalid ID for invalid tile name.
            return ["0"]
        def setTileID(self, key, value):
            tileName = key[1]
            sid = value[0]
            mat = TILE_PREFIX_MATERIAL + sid
            self.c.setConst("TILE", tileName)
            self.c.set("node.$SCENE.$TILE.material", mat)
            # Store.
            self.ids[tileName] = int(sid)
