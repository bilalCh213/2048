import pyglet
import block
import random
import math

positions = [
    [128*0, 128*0], # 00
    [128*1, 128*0], # 01
    [128*2, 128*0], # 02
    [128*3, 128*0], # 03
    [128*0, 128*1], # 04
    [128*1, 128*1], # 05
    [128*2, 128*1], # 06
    [128*3, 128*1], # 07
    [128*0, 128*2], # 08
    [128*1, 128*2], # 09
    [128*2, 128*2], # 10
    [128*3, 128*2], # 11
    [128*0, 128*3], # 12
    [128*1, 128*3], # 13
    [128*2, 128*3], # 14
    [128*3, 128*3], # 15
]
# 12 13 14 15
# 08 09 10 11
# 04 05 06 07
# 00 01 02 03

moveDownIndexes = [ 3, 7, 11, 15, 2, 6, 10, 14, 1, 5, 9, 13, 0, 4, 8, 12 ]

class BlockManager:
    blocks = []
    lerpFactor = 0.0

    def __init__(self, lerpFactor):
        self.lerpFactor = lerpFactor
        self.add()

    def reset(self):
        self.blocks.clear()
        self.add()

    def getFromAbsolutePosition(self, pos, exception = -1):
        d = 20
        for b in self.blocks:
            if b.x > pos[0] - d and b.x < pos[0] + d and b.y > pos[1] - d and b.y < pos[1] + d and b.toX == pos[0] and b.toY == pos[1] and b != exception:
                return b
        return -1

    def getFromPosition(self, pos, exception = -1):
        for b in self.blocks:
            if b.toX == pos[0] and b.toY == pos[1] and b != exception:
                return b
        return -1

    def add(self):
        emptyPositions = []
        for p in positions:
            if self.getFromPosition(p) == -1:
                emptyPositions.append(p)

        if len(emptyPositions) == 0:
            return
        
        r = math.floor(random.random() * len(emptyPositions))
        self.blocks.append(block.Block(index = 0, x = emptyPositions[r][0], y = emptyPositions[r][1], lerpFactor = self.lerpFactor))

    def isClashing(self, b1):
        for b2 in self.blocks:
            if b1 != b2 and b1.toX == b2.toX and b1.toY == b2.toY:
                return True
        return False

    def processMove(self, dir):
        isThereAnyMovement = False
        if dir == -1:
            for i in range(len(positions)):
                b1 = self.getFromAbsolutePosition(positions[i])
                if b1 != -1:
                    b2 = self.getFromAbsolutePosition(positions[i], b1)
                    if b2 != -1 and b1.index == b2.index:
                        b1.upgrade()
                        self.blocks.remove(b2)
                        
        elif dir == 0: # UP
            for i in reversed(moveDownIndexes):
                b1 = self.getFromPosition(positions[i])
                if b1 != -1:
                    b2 = self.getFromPosition([positions[i][0], positions[i][1] + 128], b1)
                    if b2 == -1:
                        b2 = self.getFromAbsolutePosition([positions[i][0], positions[i][1] + 128], b1)
                    if b2 != -1 and b1.index == b2.index:
                        b1.toY = b2.toY
                        isThereAnyMovement = True

                        for offset in range(128, 128*4, 128):
                            bi = self.getFromPosition([b1.toX, b1.toY - offset])
                            if bi != -1:
                                self.moveWithValidation(bi, dir)
        elif dir == 1: # DOWN
            for i in moveDownIndexes:
                b1 = self.getFromPosition(positions[i])
                if b1 != -1:
                    b2 = self.getFromPosition([positions[i][0], positions[i][1] - 128], b1)
                    if b2 == -1:
                        b2 = self.getFromAbsolutePosition([positions[i][0], positions[i][1] - 128], b1)
                    if b2 != -1 and b1.index == b2.index:
                        b1.toY = b2.toY
                        isThereAnyMovement = True

                        for offset in range(128, 128*4, 128):
                            bi = self.getFromPosition([b1.toX, b1.toY + offset])
                            if bi != -1:
                                self.moveWithValidation(bi, dir)
        elif dir == 2: # LEFT
            for p in positions:
                b1 = self.getFromPosition(p)
                if b1 != -1:
                    b2 = self.getFromPosition([p[0] - 128, p[1]], b1)
                    if b2 == -1:
                        b2 = self.getFromAbsolutePosition([p[0] - 128, p[1]], b1)
                    if b2 != -1 and b1.index == b2.index:
                        b1.toX = b2.toX
                        isThereAnyMovement = True

                        for offset in range(128, 128*4, 128):
                            bi = self.getFromPosition([b1.toX + offset, b1.toY])
                            if bi != -1:
                                self.moveWithValidation(bi, dir)
        elif dir == 3: # RIGHT
            for p in reversed(positions):
                b1 = self.getFromPosition(p)
                if b1 != -1:
                    b2 = self.getFromPosition([p[0] + 128, p[1]], b1)
                    if b2 == -1:
                        b2 = self.getFromAbsolutePosition([p[0] + 128, p[1]], b1)
                    if b2 != -1 and b1.index == b2.index:
                        b1.toX = b2.toX
                        isThereAnyMovement = True

                        for offset in range(128, 128*4, 128):
                            bi = self.getFromPosition([b1.toX - offset, b1.toY])
                            if bi != -1:
                                self.moveWithValidation(bi, dir)
        return isThereAnyMovement

    def moveWithValidation(self, b, dir):
        if dir == 0 or dir == 3:
            rank = 3
        elif dir == 1 or dir == 2:
            rank = 0
        if dir == 0 or dir == 1:
            b.x = b.toX
        elif dir == 2 or dir == 3:
            b.y = b.toY
        
        while True:
            if dir == 0 or dir == 1:
                b.toY = 128 * rank
            elif dir == 2 or dir == 3:
                b.toX = 128 * rank
            
            if not self.isClashing(b):
                d = 20
                if b.x > b.toX - d and b.x < b.toX + d and b.y > b.toY - d and b.y < b.toY + d:
                    return False
                else:
                    return True
            else:
                if dir == 0 or dir == 3:
                    rank = rank - 1
                    if rank < 0:
                        return False
                elif dir == 1 or dir == 2:
                    rank = rank + 1
                    if rank > 3:
                        return False
        return False

    def isAnyMoveLeft(self):
        for p in positions:
            if self.getFromPosition(p) == -1:
                return True
        for i in range(len(positions)-1):
            b1 = self.getFromPosition(positions[i])
            b2 = self.getFromPosition(positions[i+1])
            b3 = self.getFromPosition(positions[moveDownIndexes[i]])
            b4 = self.getFromPosition(positions[moveDownIndexes[i+1]])
            if (b1.toY == b2.toY and b1.index == b2.index) or (b3.toX == b4.toX and b3.index == b4.index):
                return True
        return False

    def on_key_press(self, k):
        isThereAnyMovement = False
        if k == pyglet.window.key.UP or k == pyglet.window.key.W:
            for i in reversed(moveDownIndexes):
                b = self.getFromPosition(positions[i])
                if b != -1:
                    if self.moveWithValidation(b, 0):
                        isThereAnyMovement = True
            if self.processMove(0):
                isThereAnyMovement = True

            if isThereAnyMovement:
                self.add()

        elif k == pyglet.window.key.DOWN or k == pyglet.window.key.S:
            for i in moveDownIndexes:
                b = self.getFromPosition(positions[i])
                if b != -1:
                    if self.moveWithValidation(b, 1):
                        isThereAnyMovement = True
            if self.processMove(1):
                isThereAnyMovement = True
            
            if isThereAnyMovement:
                self.add()

        elif k == pyglet.window.key.LEFT or k == pyglet.window.key.A:
            for p in positions:
                b = self.getFromPosition(p)
                if b != -1:
                    if self.moveWithValidation(b, 2):
                        isThereAnyMovement = True
            if self.processMove(2):
                isThereAnyMovement = True
            
            if isThereAnyMovement:
                self.add()

        elif k == pyglet.window.key.RIGHT or k == pyglet.window.key.D:
            for p in reversed(positions):
                b = self.getFromPosition(p)
                if b != -1:
                    if self.moveWithValidation(b, 3):
                        isThereAnyMovement = True
            if self.processMove(3):
                isThereAnyMovement = True
            
            if isThereAnyMovement:
                self.add()

    def update(self, deltaTime):
        for b in self.blocks:
            b.update(deltaTime)
        self.processMove(-1)

        return self.isAnyMoveLeft()

    def checkWin(self):
        for b in self.blocks:
            if b.index == 10:
                return True
        return False

    def draw(self):
        for b in self.blocks:
            b.draw()
