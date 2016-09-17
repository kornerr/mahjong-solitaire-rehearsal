
from pymjin2 import *

class LayoutImpl(object):
    def __init__(self, c):
        self.c = c
    def __del__(self):
        self.c = None
    def setParseFileName(self, key, value):
        print "setParseFileName", key, value

class Layout(object):
    def __init__(self, sceneName, nodeName, env):
        self.c = EnvironmentClient(env, "Layout")
        self.impl = LayoutImpl(self.c)
        self.c.setConst("SCENE", sceneName)
        # API.
        self.c.provide("layout.parseFileName", self.impl.setParseFileName)
    def __del__(self):
        # Tear down.
        self.c.clear()
        # Destroy.
        del self.impl
        del self.c

def SCRIPT_CREATE(sceneName, nodeName, env):
    return Layout(sceneName, nodeName, env)

def SCRIPT_DESTROY(instance):
    del instance

