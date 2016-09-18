# Create tiles.
CLASS Main
    PART IMPL
        positions = self.c.get("layout.positions")
        # Create tiles.
        for p in positions:
            self.c.setConst("TILE", p)
            self.c.set("tile.$TILE.position", p)
