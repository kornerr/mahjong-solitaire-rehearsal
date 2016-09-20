
from pymjin2 import *

# BEGIN FEATURE MAIN_LAYOUT
MAIN_LAYOUT     = "X_shaped"
#MAIN_LAYOUT     = "cat"
#MAIN_LAYOUT     = "default"
MAIN_LAYOUT_DIR = "layouts"
MAIN_LAYOUT_EXT = "layout"
MAIN_RESOLVER   = "pathResolver.MainResolver"
# END FEATURE MAIN_LAYOUT
MAIN_SOUND_START = "soundBuffer.default.start"

class MainImpl(object):
    def __init__(self, c):
        self.c = c
        self.isOn = False
    def __del__(self):
        self.c = None
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
        for p in positions:
            self.c.setConst("TILE", p)
            # Generate random number in [1; 9] range.
            id = rand() % 9 + 1
            self.c.set("tile.$TILE.id", str(id))
# END FEATURE IDENTIFY_TILES

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

