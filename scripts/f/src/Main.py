
from pymjin2 import *

# MJIN2_FEATURE MAIN_LAYOUT/CONST
# MJIN2_FEATURE IDENTIFY_TILES/CONST
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
        # MJIN2_FEATURE MAIN_LAYOUT/IMPL
        # MJIN2_FEATURE MAIN_LAYOUT_TILES/IMPL
        # MJIN2_FEATURE CENTER_TILES/IMPL
        # MJIN2_FEATURE IDENTIFY_TILES/IMPL
        # MJIN2_FEATURE AVAILABLE_TILES/IMPL

class Main(object):
    def __init__(self, sceneName, nodeName, env):
        self.c = EnvironmentClient(env, "Main")
        self.impl = MainImpl(self.c)
        self.c.setConst("SCENE",    sceneName)
        self.c.setConst("NODE",     nodeName)
        self.c.setConst("SNDSTART", MAIN_SOUND_START)
        self.c.listen("input.SPACE.key", "1", self.impl.onSpace)
        # MJIN2_FEATURE MAIN_LAYOUT/INIT
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

