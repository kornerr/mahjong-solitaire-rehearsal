# Depict selected tile.
CLASS Tiles
    PART CONST
        TILE_MATERIAL_SELECTED = "tile0{0}_selected"
    PART INIT
        self.c.listen("node.$SCENE..selected", None, self.impl.onTileSelection)
        self.impl.lastSelectedTile = None
    PART IMPL
        def onTileSelection(self, key, value):
            tileName = key[2]
            if (self.lastSelectedTile):
                # Do nothing.
                if (tileName == self.lastSelectedTile):
                    return
                # Deselect previously selected tile.
                self.setTileSelected(self.lastSelectedTile, False)
            # Select tile.
            self.setTileSelected(tileName, True)
            self.lastSelectedTile = tileName
        def setTileSelected(self, tileName, state):
            id = self.ids[tileName]
            mat = TILE_PREFIX_MATERIAL + str(id)
            if (state):
                mat = TILE_MATERIAL_SELECTED.format(id)
            self.c.setConst("TILE", tileName)
            self.c.set("node.$SCENE.$TILE.material", mat)
