# Provide "main.replayStartSound"
CLASS Main
    PART CONST
        MAIN_START_SOUND_API = "main.replayStartSound"
        MAIN_START_SOUND     = "soundBuffer.default.start"
    PART INIT
        self.c.setConst("START_SOUND", MAIN_START_SOUND)
        self.c.provide(MAIN_START_SOUND_API, self.setReplayStartSound)
    PART IMPL
        def setReplayStartSound(self, key, value):
            self.c.set("$START_SOUND.state", "play")
            self.c.report(MAIN_START_SOUND_API, "0")
