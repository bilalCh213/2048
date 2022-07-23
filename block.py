
import pyglet

def lerp(a, b, factor):
    return a + (b - a) * factor

sheet = pyglet.image.load("2048spritesheet.png")
blocks = [
    sheet.get_region(0,     128*2,  128, 128), #2 - 0
    sheet.get_region(128,   128*2,  128, 128), #4 - 1
    sheet.get_region(128*2, 128*2,  128, 128), #8 - 2
    sheet.get_region(128*3, 128*2,  128, 128), #16 - 3
    sheet.get_region(0,     128,    128, 128), #32 - 4
    sheet.get_region(128,   128,    128, 128), #64 - 5
    sheet.get_region(128*2, 128,    128, 128), #128 - 6
    sheet.get_region(128*3, 128,    128, 128), #256 - 7
    sheet.get_region(0,     0,      128, 128), #512 - 8
    sheet.get_region(128,   0,      128, 128), #1024 - 9
    sheet.get_region(128*2, 0,      128, 128), #2048 - 10
    sheet.get_region(128*3, 0,      128, 128), #4096 - 11
]

class Block(pyglet.sprite.Sprite):
    index = 0
    toX = 0
    toY = 0
    lerpFactor = 0

    def __init__(self, index, x, y, lerpFactor):
        super(Block, self).__init__(blocks[index], x, y)
        self.scale = 0.0
        self.index = index
        self.toX = x
        self.toY = y
        self.lerpFactor = lerpFactor

    def update(self, deltaTime):
        self.scale = lerp(self.scale, 1.0, self.lerpFactor * deltaTime)
        self.x = lerp(self.x, self.toX, self.lerpFactor * deltaTime)
        self.y = lerp(self.y, self.toY, self.lerpFactor * deltaTime)

    def upgrade(self):
        self.index = self.index + 1
        self.image = blocks[self.index]
        self.scale = 1.25