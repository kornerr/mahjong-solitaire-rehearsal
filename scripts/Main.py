
from pymjin2 import *

# BEGIN FEATURE MAIN_LAYOUT
#MAIN_LAYOUT     = "X_shaped"
MAIN_LAYOUT     = "test"
#MAIN_LAYOUT     = "cat"
#MAIN_LAYOUT     = "default"
MAIN_LAYOUT_DIR = "layouts"
MAIN_LAYOUT_EXT = "layout"
MAIN_RESOLVER   = "pathResolver.MainResolver"
# END FEATURE MAIN_LAYOUT
# BEGIN FEATURE IDENTIFY_TILES
MAIN_TILE_IDS = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# END FEATURE IDENTIFY_TILES
MAIN_SOUND_START = "soundBuffer.default.start"

class MainImpl(object):
    def __init__(self, c):
        self.c = c
        self.isOn = False
    def __del__(self):
        self.c = None
# BEGIN FEATURE MAIN_RESULT
    def onStats(self, key, value):
        print "onStats", key, value
        hasTiles = int(value[0])
        hasMatches = int(value[1])
        print "has tiles/matches", hasTiles, hasMatches
        if (not hasTiles):
            print "Victory"
        elif (not hasMatches):
            print "Loss"
# END FEATURE MAIN_RESULT
    def onSpace(self, key, value):
        if self.isOn:
            return
        self.isOn = True
        print "Space pressed. Start the game"
        self.c.set("$SNDSTART.state", "play")
# BEGIN FEATURE MAIN_LAYOUT
        fileName = "{0}/{1}.{2}".format(MAIN_LAYOUT_DIR,
                                        MAIN_LAYOUT,
                                        MAIN_LAYOUT_EXT)
        self.c.set("$RESOLVER.resolveFileNameAbs", fileName)
        fileNameAbs = self.c.get("$RESOLVER.fileNameAbs")
        self.c.set("layout.parseFileName", fileNameAbs)
        errors = self.c.get("layout.errors")
        if (len(errors)):
            print "Cannot proceed, because there are errors:"
            print errors
            return
# END FEATURE MAIN_LAYOUT
# BEGIN FEATURE MAIN_LAYOUT_TILES
        positions = self.c.get("layout.positions")
        # Create tiles.
        for p in positions:
            self.c.setConst("TILE", p)
            self.c.set("tile.$TILE.position", p)
# END FEATURE MAIN_LAYOUT_TILES
# BEGIN FEATURE CENTER_TILES
        dim = self.c.get("layout.dimensions")
        self.c.set("tiles.center", dim)
# END FEATURE CENTER_TILES
# BEGIN FEATURE IDENTIFY_TILES
        i = 1
        vpos = list(positions)
        # Distribute IDs so that each ID has a pair.
        while (len(vpos)):
            i = i + 1
            positionID = rand() % len(vpos)
            idsID = i / 2 - 1
            # Reset i.
            if (idsID >= len(MAIN_TILE_IDS)):
                i = 2
                idsID = 0
            pos = vpos[positionID]
            id = MAIN_TILE_IDS[idsID]
            # Assign.
            self.c.setConst("TILE", pos)
            self.c.set("tile.$TILE.id", str(id))
            del vpos[positionID]
# END FEATURE IDENTIFY_TILES
# BEGIN FEATURE AVAILABLE_TILES
        self.c.set("tiles.refreshAvailability", "1")
# END FEATURE AVAILABLE_TILES

class Main(object):
    def __init__(self, sceneName, nodeName, env):
        self.c = EnvironmentClient(env, "Main")
        self.impl = MainImpl(self.c)
        self.c.setConst("SCENE",    sceneName)
        self.c.setConst("NODE",     nodeName)
        self.c.setConst("SNDSTART", MAIN_SOUND_START)
        self.c.listen("input.SPACE.key", "1", self.impl.onSpace)
# BEGIN FEATURE MAIN_LAYOUT
        self.c.setConst("RESOLVER", MAIN_RESOLVER)
# END FEATURE MAIN_LAYOUT
# BEGIN FEATURE MAIN_RESULT
        self.c.listen("tiles.stats", None, self.impl.onStats)
# END FEATURE MAIN_RESULT
    def __del__(self):
        # Tear down.
        self.c.clear()
        # Destroy.
        del self.impl
        del self.c

def SCRIPT_CREATE(sceneName, nodeName, env):
    return Main(sceneName, nodeName, env)

def SCRIPT_DESTROY(instance):
    del instance

