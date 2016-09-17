
from pymjin2 import *

LAYOUT_DEFAULT_WIDTH  = 32
LAYOUT_DEFAULT_HEIGHT = 16
LAYOUT_PREFIX_VERSION = "kmahjongg-layout-v"
LAYOUT_VERSIONS       = ["1.0",
                         "1.1"]
# Layout 1.1 related prefixes.
LAYOUT_PREFIX_DEPTH   = "d"
LAYOUT_PREFIX_HEIGHT  = "h"
LAYOUT_PREFIX_WIDTH   = "w"

class LayoutImpl(object):
    def __init__(self, c):
        self.c = c
    def __del__(self):
        self.c = None
    def parseField(self, lines, width, height):
        print "w/h", width, height
        print "field", lines
    def parseLines(self, lines):
        # Field dimensions.
        depth  = 0
        height = LAYOUT_DEFAULT_HEIGHT
        width  = LAYOUT_DEFAULT_WIDTH
        # Buffers.
        fieldLines = []
        fieldLineID = 0
        fields = []
        # Parse.
        for ln in lines:
            # Ignore comment.
            if ln.startswith("#"):
                continue
            sln = ln.strip()
            # BEGIN Constants.
            if sln.startswith(LAYOUT_PREFIX_VERSION):
                version = sln.split(LAYOUT_PREFIX_VERSION)[1]
                # TODO: check version
            elif sln.startswith(LAYOUT_PREFIX_DEPTH):
                depth = int(sln.split(LAYOUT_PREFIX_DEPTH)[1])
            elif sln.startswith(LAYOUT_PREFIX_HEIGHT):
                height = int(sln.split(LAYOUT_PREFIX_HEIGHT)[1])
            elif sln.startswith(LAYOUT_PREFIX_WIDTH):
                width = int(sln.split(LAYOUT_PREFIX_WIDTH)[1])
            # END Constants.
            # BEGIN Field.
            else:
                fieldLines.append(sln)
                fieldLineID = fieldLineID + 1
                if (fieldLineID >= height):
                    # Collect field layers.
                    fields.append(fieldLines)
                    # Reset buffers.
                    fieldLines = []
                    fieldLineID = 0
            # END Field.
        # TODO: check depth
        # TODO: check number of tiles
        #self.parseField(fieldLines, width, height)
        print "w/h/d", width, height, depth
        print "fields nb", len(fields)
    def setParseFileName(self, key, value):
        fileName = value[0]
        with open(fileName, "r") as f:
            lines = f.readlines()
            self.parseLines(lines)

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

