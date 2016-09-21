
from pymjin2 import *

TILE_MODEL           = "models/tile.osgt"
TILE_PREFIX_MATERIAL = "tile0"
# MJIN2_FEATURE AVAILABLE_TILES/CONST
# MJIN2_FEATURE TILES_SELECTION/CONST

class TilesImpl(object):
    def __init__(self, c, nodeName):
        self.c = c
        self.nodeParent = nodeName
        self.tiles = { }
        # MJIN2_FEATURE TILES_POSITION/INIT
    def __del__(self):
        self.c = None
    # MJIN2_FEATURE CENTER_TILES/IMPL
    # MJIN2_FEATURE IDENTIFY_TILES/IMPL
    # MJIN2_FEATURE AVAILABLE_TILES/IMPL
    # MJIN2_FEATURE TILES_POSITION/IMPL
    # MJIN2_FEATURE TILES_SELECTION/IMPL
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
        # MJIN2_FEATURE TILES_POSITION/TRANSLATE
        self.c.set("node.$SCENE.$TILE.position", pos)

class Tiles(object):
    def __init__(self, sceneName, nodeName, env):
        self.c = EnvironmentClient(env, "Tiles")
        self.impl = TilesImpl(self.c, nodeName)
        self.c.setConst("SCENE", sceneName)
        self.c.setConst("NODE",  nodeName)
        # API.
        self.c.provide("tiles.delete", self.impl.setDelete)
        self.c.provide("tile..position", self.impl.setPosition)
        # MJIN2_FEATURE CENTER_TILES/INIT
        # MJIN2_FEATURE IDENTIFY_TILES/INIT
        # MJIN2_FEATURE AVAILABLE_TILES/INIT
        # MJIN2_FEATURE TILES_SELECTION/INIT
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

