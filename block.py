import pygame, sys, const
from pygame.locals import *
from utils import *

class Block(pygame.sprite.Sprite):
    def __init__(self, blockType, baseRowIdx, baseColIdx, blockShape, blockRotate, blockGroupIdx, width, height, relPos):
        super().__init__()
        self.blockType = blockType
        self.blockShape = blockShape
        self.blockRotate = blockRotate
        self.blockGroupIdx = blockGroupIdx
        self.baseRowIdx = baseRowIdx
        self.baseColIdx = baseColIdx
        self.width = width
        self.height = height
        self.relPos = relPos
        self.blink = False
        self.blinkCount = 0
        self.hasShadow = False
        self.loadImage()
        self.updateImagePos()

    def setBaseIndex(self, baseRow, baseCol):
        self.baseRowIdx = baseRow
        self.baseColIdx = baseCol

    def getBlockConfigIndex(self):
        return const.BLOCK_SHAPES[self.blockShape][self.blockRotate][self.blockGroupIdx]

    @property
    def rowIdx(self):
        return self.baseRowIdx + self.getBlockConfigIndex()[0]

    @property
    def colIdx(self):
        return self.baseColIdx + self.getBlockConfigIndex()[1]

    def loadImage(self):
        self.image = pygame.image.load(const.BLOCK_RES[self.blockType])
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def updateImagePos(self):
        self.rect = self.image.get_rect()
        self.rect.left = self.relPos[0] + self.width * self.colIdx
        self.rect.top = self.relPos[1] + self.height * self.rowIdx

    def getIndex(self):
        return (int(self.rowIdx), int(self.colIdx))

    def getNextIndex(self):
        return (int(self.rowIdx + 1), int(self.colIdx))

    def drop(self, rowsNum):
            self.baseRowIdx += rowsNum

    def isLeftBoundary(self):
        return self.colIdx == 0

    def isRightBoundary(self):
        return self.colIdx == const.GAME_COL - 1

    def moveLeft(self):
        self.baseColIdx -= 1

    def moveRight(self):
        self.baseColIdx += 1

    def rotate(self):
        self.blockRotate += 1
        if self.blockRotate >= len(const.BLOCK_SHAPES[self.blockShape]):
            self.blockRotate = 0

    def setShadow(self, b):
        self.hasShadow = b

    def startBlink(self):
        self.blink = True
        self.blinkTime = getCurrentTime()

    # Check if the block is to be eliminated
    def update(self):
        if self.blink:
            diffTime = getCurrentTime() - self.blinkTime
            self.blinkCount = int(diffTime / 30)

    def drawSelf(self, surface):
        surface.blit(self.image, self.rect)

    def draw(self, surface):
        self.updateImagePos()
        if self.blink and self.blinkCount % 2 == 0:
            return
        self.drawSelf(surface)
