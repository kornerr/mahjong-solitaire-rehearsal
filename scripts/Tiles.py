
from pymjin2 import *

TILE_MODEL           = "models/tile.osgt"
TILE_PREFIX_MATERIAL = "tile0"
# BEGIN FEATURE AVAILABLE_TILES
TILE_MATERIAL_UNAVAILABLE = "tile0{0}_unavailable"
# END FEATURE AVAILABLE_TILES
# BEGIN FEATURE TILES_SELECTION
TILE_MATERIAL_SELECTED = "tile0{0}_selected"
# END FEATURE TILES_SELECTION

class TilesImpl(object):
    def __init__(self, c, nodeName):
        self.c = c
        self.nodeParent = nodeName
        self.tiles = { }
# BEGIN FEATURE TILES_POSITION
        # Tile dimensions.
        self.tileDim = []
# END FEATURE TILES_POSITION
    def __del__(self):
        self.c = None
# BEGIN FEATURE CENTER_TILES
    def setCenter(self, key, value):
        w = int(value[0])
        h = int(value[1])
        offset = (w / 2.0 * self.tileDim[0] / 2.0,
                  h / 2.0 * self.tileDim[1] / 2.0 - self.tileDim[1])
        pos = "{0} {1} 0".format(-offset[0], -offset[1])
        self.c.set("node.$SCENE.$NODE.position", pos)
# END FEATURE CENTER_TILES
# BEGIN FEATURE IDENTIFY_TILES
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
# END FEATURE IDENTIFY_TILES
# BEGIN FEATURE AVAILABLE_TILES
    def refreshAvailability(self):
        for tileName in self.ids:
            state = self.tileIsAvailable(tileName)
            self.setTileAvailable(tileName, state)
    def setRefreshAvailability(self, key, value):
        self.refreshAvailability()
    def setTileAvailable(self, tileName, state):
        id = self.ids[tileName]
        mat = TILE_PREFIX_MATERIAL + str(id)
        if (not state):
            mat = TILE_MATERIAL_UNAVAILABLE.format(id)
        self.c.setConst("TILE", tileName)
        # Set corresponding material.
        self.c.set("node.$SCENE.$TILE.material", mat)
        # Make available tile selectable.
        val = ("1" if state else "0")
        self.c.set("node.$SCENE.$TILE.selectable", val)
    def tileHasNeighbours(self, tileName, offsetDepth, offsetRow):
        p = tileName.split(" ")
        pos = (int(p[0]), int(p[1]), int(p[2]))
        for offsetColumn in xrange(-1, 2):
            neighbourName = "{0} {1} {2}".format(pos[0] + offsetDepth,
                                                 pos[1] + offsetColumn,
                                                 pos[2] + offsetRow)
            if (neighbourName in self.ids):
                return True
        return False
    def tileIsAvailable(self, tileName):
        # Tile is blocked at both sides.
        left  = self.tileHasNeighbours(tileName, 0, -2)
        right = self.tileHasNeighbours(tileName, 0, 2)
        if (left and right):
            return False
        # Tile is blocked at the top.
        for column in xrange(-1, 2):
            if (self.tileHasNeighbours(tileName, 1, column)):
                return False
        # Tile is free.
        return True
# END FEATURE AVAILABLE_TILES
# BEGIN FEATURE TILES_POSITION
    def calculateTileDimOnce(self):
        if (len(self.tileDim)):
            return
        bb = self.c.get("node.$SCENE.$TILE.bbox")[0].split(" ")
        self.tileDim = [float(bb[1]) - float(bb[0]),
                        float(bb[3]) - float(bb[2]),
                        float(bb[5]) - float(bb[4])]
# END FEATURE TILES_POSITION
# BEGIN FEATURE TILES_SELECTION
    def matchTiles(self, tile1, tile2):
        id1 = self.ids[tile1]
        id2 = self.ids[tile2]
        # Tiles do not match.
        if (id1 != id2):
            return False
        # Delete matching tiles.
        self.deleteTile(tile1)
        self.deleteTile(tile2)
        self.refreshAvailability()
        return True
    def onTileSelection(self, key, value):
        tileName = key[2]
        if (self.lastSelectedTile):
            # Do nothing.
            if (tileName == self.lastSelectedTile):
                return
            # Deselect previously selected tile.
            self.setTileSelected(self.lastSelectedTile, False)
            # Match.
            if (self.matchTiles(self.lastSelectedTile, tileName)):
                self.lastSelectedTile = None
                return
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
# END FEATURE TILES_SELECTION
    def createTileOnce(self, tileName):
        if (tileName in self.tiles):
            return
        self.c.set("node.$SCENE.$TILE.parent", self.nodeParent)
        self.c.set("node.$SCENE.$TILE.model",  TILE_MODEL)
        # Default material.
        mat = TILE_PREFIX_MATERIAL + "1"
        self.c.set("node.$SCENE.$TILE.material", mat)
    def deleteTile(self, tileName):
        self.c.setConst("TILE", tileName)
        self.c.set("node.$SCENE.$TILE.parent", "")
# BEGIN FEATURE IDENTIFY_TILES
        del self.ids[tileName]
# END FEATURE IDENTIFY_TILES
    def setPosition(self, key, value):
        tileName = key[1]
        self.c.setConst("TILE", tileName)
        self.createTileOnce(tileName)
        # Convert "depth row column" into "x y z".
        p = value[0].split(" ")
        pos = "{0} {1} {2}".format(p[2], p[1], p[0])
# BEGIN FEATURE TILES_POSITION
        self.calculateTileDimOnce()
        k = 0.5
        x = float(p[2]) * self.tileDim[0] * k
        y = float(p[1]) * self.tileDim[1] * k
        z = float(p[0]) * self.tileDim[2]
        pos = "{0} {1} {2}".format(x, y, z)
# END FEATURE TILES_POSITION
        self.c.set("node.$SCENE.$TILE.position", pos)

class Tiles(object):
    def __init__(self, sceneName, nodeName, env):
        self.c = EnvironmentClient(env, "Tiles")
        self.impl = TilesImpl(self.c, nodeName)
        self.c.setConst("SCENE", sceneName)
        self.c.setConst("NODE",  nodeName)
        # API.
        self.c.provide("tile..position", self.impl.setPosition)
# BEGIN FEATURE CENTER_TILES
        self.c.provide("tiles.center", self.impl.setCenter)
# END FEATURE CENTER_TILES
# BEGIN FEATURE IDENTIFY_TILES
        self.c.provide("tile..id", self.impl.setTileID, self.impl.tileID)
        self.impl.ids = {}
# END FEATURE IDENTIFY_TILES
# BEGIN FEATURE AVAILABLE_TILES
        self.c.provide("tiles.refreshAvailability",
                       self.impl.setRefreshAvailability)
# END FEATURE AVAILABLE_TILES
# BEGIN FEATURE TILES_SELECTION
        self.c.listen("node.$SCENE..selected", None, self.impl.onTileSelection)
        self.impl.lastSelectedTile = None
# END FEATURE TILES_SELECTION
    def __del__(self):
        # Tear down.
        self.c.clear()
        # Destroy.
        del self.impl
        del self.c

def SCRIPT_CREATE(sceneName, nodeName, env):
    return Tiles(sceneName, nodeName, env)

def SCRIPT_DESTROY(instance):
    del instance

