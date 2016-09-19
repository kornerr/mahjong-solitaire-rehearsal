
from pymjin2 import *

TILE_MODEL           = "models/tile.osgt"
TILE_PREFIX_MATERIAL = "tile0"

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
# BEGIN FEATURE TILES_POSITION
    def calculateTileDimOnce(self):
        if (len(self.tileDim)):
            return
        bb = self.c.get("node.$SCENE.$TILE.bbox")[0].split(" ")
        self.tileDim = [float(bb[1]) - float(bb[0]),
                        float(bb[3]) - float(bb[2]),
                        float(bb[5]) - float(bb[4])]
# END FEATURE TILES_POSITION
    def createTileOnce(self, tileName):
        if (tileName in self.tiles):
            return
        self.c.set("node.$SCENE.$TILE.parent", self.nodeParent)
        self.c.set("node.$SCENE.$TILE.model",  TILE_MODEL)
        # Default material.
        mat = TILE_PREFIX_MATERIAL + "1"
        self.c.set("node.$SCENE.$TILE.material", mat)
    def setDelete(self, key, value):
        print "setDelete", key, value
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
        pos = "{0} {1} {2}".format(float(p[2]) * self.tileDim[0] * k,
                                   float(p[1]) * self.tileDim[1] * k,
                                   float(p[0]) * self.tileDim[2])
        print "pos", pos
        # END FEATURE TILES_POSITION
        self.c.set("node.$SCENE.$TILE.position", pos)

class Tiles(object):
    def __init__(self, sceneName, nodeName, env):
        self.c = EnvironmentClient(env, "Tiles")
        self.impl = TilesImpl(self.c, nodeName)
        self.c.setConst("SCENE", sceneName)
        # API.
        self.c.provide("tiles.delete", self.impl.setDelete)
        self.c.provide("tile..position", self.impl.setPosition)
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

