
from pymjin2 import *


class TilesImpl(object):
    def __init__(self, c):
        self.c = c
    def __del__(self):
        self.c = None

class Tiles(object):
    def __init__(self, sceneName, nodeName, env):
        self.c = EnvironmentClient(env, "Tiles")
        self.impl = TilesImpl(self.c)
        self.c.setConst("SCENE", sceneName)
        # API.
        #self.c.provide("layout.parseFileName", self.impl.setParseFileName)
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

