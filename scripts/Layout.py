
from pymjin2 import *

LAYOUT_DEFAULT_WIDTH  = 32
LAYOUT_DEFAULT_HEIGHT = 16
LAYOUT_PREFIX_VERSION = "kmahjongg-layout-v"
# Layout 1.1 related prefixes.
LAYOUT_PREFIX_DEPTH   = "d"
LAYOUT_PREFIX_HEIGHT  = "h"
LAYOUT_PREFIX_WIDTH   = "w"
# BEGIN FEATURE LAYOUT_ERRORS
LAYOUT_VERSIONS = ["1.0",
                   "1.1"]
# END FEATURE LAYOUT_ERRORS

class LayoutImpl(object):
    def __init__(self, c):
        self.c = c
        self.positions = []
    def __del__(self):
        self.c = None
# BEGIN FEATURE LAYOUT_DIMENSIONS
    def dimensions(self, key):
        return self.dim
# END FEATURE LAYOUT_DIMENSIONS
# BEGIN FEATURE LAYOUT_ERRORS
    def errors(self, key):
        return self.errlist
# END FEATURE LAYOUT_ERRORS
    def parseFields(self, fields, width, height):
        self.positions = []
        for i in xrange(0, len(fields)):
            field = fields[i]
            for row in xrange(0, height - 1):
                for column in xrange(0, width - 1):
                    # Detect tile.
                    if ((field[row][column]         == "1") and
                        (field[row][column + 1]     == "2") and
                        (field[row + 1][column]     == "4") and
                        (field[row + 1][column + 1] == "3")):
                        self.positions.append("{0} {1} {2}".format(i,
                                                                   row,
                                                                   column))
    def parseLines(self, lines):
# BEGIN FEATURE LAYOUT_ERRORS
        self.errlist = []
# END FEATURE LAYOUT_ERRORS
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
# BEGIN FEATURE LAYOUT_ERRORS
                if version not in LAYOUT_VERSIONS:
                    self.errlist.append("Unsupported version: '{0}'".format(version))
# END FEATURE LAYOUT_ERRORS
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
# BEGIN FEATURE LAYOUT_DIMENSIONS
        self.dim = [str(width),
                    str(height)]
# END FEATURE LAYOUT_DIMENSIONS
# BEGIN FEATURE LAYOUT_ERRORS
        if depth and len(fields) != depth:
            err = "Invalid field depth. Got/expected: '{0}/{1}'"
            self.errlist.append(err.format(len(fields),
                                           depth))
# END FEATURE LAYOUT_ERRORS
        self.parseFields(fields, width, height)
# BEGIN FEATURE LAYOUT_ERRORS
        n = len(self.positions)
        if (n % 2):
            err = "Number of positions is not even: '{0}'"
            self.errlist.append(err.format(n))
# END FEATURE LAYOUT_ERRORS
    def pos(self, key):
        return self.positions
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
        self.c.setConst("NODE",  nodeName)
        # API.
        self.c.provide("layout.parseFileName", self.impl.setParseFileName)
        self.c.provide("layout.positions", None, self.impl.pos)
# BEGIN FEATURE LAYOUT_DIMENSIONS
        self.c.provide("layout.dimensions", None, self.impl.dimensions)
        self.impl.dim = ["0", "0"]
# END FEATURE LAYOUT_DIMENSIONS
# BEGIN FEATURE LAYOUT_ERRORS
        self.c.provide("layout.errors", None, self.impl.errors)
        self.impl.errlist = []
# END FEATURE LAYOUT_ERRORS
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

