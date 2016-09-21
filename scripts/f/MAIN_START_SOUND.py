# Provide "main.replayStartSound"
CLASS Main
    PART CONST
        MAIN_SOUND_START = "soundBuffer.default.start"
    PART INIT
        self.c.setConst("SNDSTART", MAIN_SOUND_START)
        self.c.provide("main.replayStartSound", self.impl.setReplayStartSound)
    PART IMPL
        def setReplayStartSound(self, key, value):
            print "setReplayStartSound"
            self.c.set("$SNDSTART.state", "play")
            self.c.report("main.replayStartSound", "0")
