
from pymjin2 import *

# MJIN2_FEATURE MAIN_START_SOUND/CONST
MAIN_SEQUENCE_START = "sequence.default.start"

class MainImpl(object):
    def __init__(self, c):
        self.c = c
        self.isOn = False
        # MJIN2_FEATURE MAIN_START_SOUND/INIT
    def __del__(self):
        self.c = None
    # MJIN2_FEATURE MAIN_START_SOUND/IMPL
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
        self.c.setConst("SCENE",    sceneName)
        self.c.setConst("NODE",     nodeName)
        self.c.listen("input.SPACE.key", "1", self.impl.onSpace)
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

