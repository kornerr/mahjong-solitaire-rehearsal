
from pymjin2 import *

MAIN_SEQUENCE_START = "sequence.default.start"
# BEGIN FEATURE MAIN_START_SOUND
MAIN_START_SOUND_API = "main.replayStartSound"
MAIN_START_SOUND     = "soundBuffer.default.start"
# END FEATURE MAIN_START_SOUND
# BEGIN FEATURE MAIN_LAYOUT
#MAIN_LAYOUT     = "X_shaped"
MAIN_LAYOUT     = "test"
#MAIN_LAYOUT     = "cat"
#MAIN_LAYOUT     = "default"
MAIN_LAYOUT_API = "main.loadLayout"
MAIN_LAYOUT_DIR = "layouts"
MAIN_LAYOUT_EXT = "layout"
MAIN_RESOLVER   = "pathResolver.MainResolver"
# END FEATURE MAIN_LAYOUT
# BEGIN FEATURE MAIN_LAYOUT_TILES
MAIN_LAYOUT_TILES_API = "main.createTiles"
# END FEATURE MAIN_LAYOUT_TILES
# BEGIN FEATURE CENTER_TILES
MAIN_CENTER_TILES_API = "main.centerTiles"
# END FEATURE CENTER_TILES

class MainImpl(object):
    def __init__(self, c):
        self.c = c
        self.isOn = False
        self.c.listen("input.SPACE.key", "1", self.onSpace)
# BEGIN FEATURE MAIN_START_SOUND
        self.c.setConst("START_SOUND", MAIN_START_SOUND)
        self.c.provide(MAIN_START_SOUND_API, self.setReplayStartSound)
# END FEATURE MAIN_START_SOUND
# BEGIN FEATURE MAIN_LAYOUT
        self.c.setConst("RESOLVER", MAIN_RESOLVER)
        self.c.provide(MAIN_LAYOUT_API, self.setLoadLayout)
# END FEATURE MAIN_LAYOUT
# BEGIN FEATURE MAIN_LAYOUT_TILES
        self.c.provide(MAIN_LAYOUT_TILES_API, self.setCreateTiles)
# END FEATURE MAIN_LAYOUT_TILES
# BEGIN FEATURE CENTER_TILES
        self.c.provide(MAIN_CENTER_TILES_API, self.setCenterTiles)
# END FEATURE CENTER_TILES
    def __del__(self):
        self.c = None
# BEGIN FEATURE MAIN_START_SOUND
    def setReplayStartSound(self, key, value):
        self.c.set("$START_SOUND.state", "play")
        self.c.report(MAIN_START_SOUND_API, "0")
# END FEATURE MAIN_START_SOUND
# BEGIN FEATURE MAIN_LAYOUT
    def setLoadLayout(self, key, value):
        fileName = "{0}/{1}.{2}".format(MAIN_LAYOUT_DIR,
                                        MAIN_LAYOUT,
                                        MAIN_LAYOUT_EXT)
        self.c.set("$RESOLVER.resolveFileNameAbs", fileName)
        fileNameAbs = self.c.get("$RESOLVER.fileNameAbs")
        self.c.set("layout.parseFileName", fileNameAbs)
        errors = self.c.get("layout.errors")
        if (len(errors)):
            print "There are errors:", errors
        # TODO: react to error.
        self.c.report(MAIN_LAYOUT_API, "0")
# END FEATURE MAIN_LAYOUT
# BEGIN FEATURE MAIN_LAYOUT_TILES
    def setCreateTiles(self, key, value):
        positions = self.c.get("layout.positions")
        # Create tiles.
        for p in positions:
            self.c.setConst("TILE", p)
            self.c.set("tile.$TILE.position", p)
        self.c.report(MAIN_LAYOUT_TILES_API, "0")
# END FEATURE MAIN_LAYOUT_TILES
# BEGIN FEATURE CENTER_TILES
    def setCenterTiles(self, key, value):
        dim = self.c.get("layout.dimensions")
        self.c.set("tiles.center", dim)
        self.c.report(MAIN_CENTER_TILES_API, "0")
# END FEATURE CENTER_TILES
    def onSpace(self, key, value):
        if self.isOn:
            return
        self.isOn = True
        print "Space pressed. Start the game"
        self.c.setConst("SEQSTART", MAIN_SEQUENCE_START)
        self.c.set("$SEQSTART.active", "1")

class Main(object):
    def __init__(self, sceneName, nodeName, env):
        self.c = EnvironmentClient(env, "Main")
        self.impl = MainImpl(self.c)
        self.c.setConst("SCENE", sceneName)
        self.c.setConst("NODE",  nodeName)
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

