
from pymjin2 import *

# BEGIN FEATURE MAIN_START_SOUND
MAIN_SOUND_START = "soundBuffer.default.start"
# END FEATURE MAIN_START_SOUND
MAIN_SEQUENCE_START = "sequence.default.start"

class MainImpl(object):
    def __init__(self, c):
        self.c = c
        self.isOn = False
    def __del__(self):
        self.c = None
# BEGIN FEATURE MAIN_START_SOUND
    def setReplayStartSound(self, key, value):
        print "setReplayStartSound"
        self.c.set("$SNDSTART.state", "play")
        self.c.report("main.replayStartSound", "0")
# END FEATURE MAIN_START_SOUND
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
# BEGIN FEATURE MAIN_START_SOUND
        self.c.setConst("SNDSTART", MAIN_SOUND_START)
        self.c.provide("main.replayStartSound", self.impl.setReplayStartSound)
# END FEATURE MAIN_START_SOUND
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

