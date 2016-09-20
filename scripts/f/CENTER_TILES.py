# Center tiles.
CLASS Main
    PART IMPL
        dim = self.c.get("layout.dimensions")
        self.c.set("tiles.center", dim)
CLASS Tiles
    PART INIT
        self.c.provide("tiles.center", self.impl.setCenter)
    PART IMPL
        def setCenter(self, key, value):
            w = int(value[0])
            h = int(value[1])
            offset = (w / 2.0 * self.tileDim[0] / 2.0,
                      h / 2.0 * self.tileDim[1] / 2.0 - self.tileDim[1])
            pos = "{0} {1} 0".format(-offset[0], -offset[1])
            self.c.set("node.$SCENE.$NODE.position", pos)
