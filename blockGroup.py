import random
import pygame.mixer
from block import *
from utils import *

import const

class BlockGroup(object):
    def GenerateBlockGroupConfig(rowIdx, colIdx, shapeIdx = -1):
        if shapeIdx == -1:
            shapeIdx = random.randint(0, len(const.BLOCK_SHAPES)-1)
        bType = random.randint(0, const.BlockType.BLOCKMAX-1)
        configList = []
        rotateIdx = 0
        for i in range(len(const.BLOCK_SHAPES[shapeIdx][rotateIdx])):
            config = {
                'blockType': bType,
                'blockShape': shapeIdx,
                'blockRotate': rotateIdx,
                'blockGroupIdx': i,
                'rowIdx': rowIdx,
                'colIdx': colIdx
            }
            configList.append(config)
        return configList

    def __init__(self, blockGroupType, width, height, blockConfigList, relPos):
        super().__init__()
        self.blocks = []
        self.blockGroupType = blockGroupType
        self.dropTime = getCurrentTime()
        self.dropInterval = 900
        self.pressTime = {}
        self.eliminate = False
        self.eliminateRow = []
        self.eliminateTime = 0
        for config in blockConfigList:
            block = Block(config['blockType'], config['rowIdx'], config['colIdx'], config['blockShape'],
                        config['blockRotate'], config['blockGroupIdx'], width, height, relPos)
            self.blocks.append(block)
        self.isPause = False
        self.isFallingDown = False

    def setDropInterval(self, dropInterval):
        self.dropInterval = dropInterval

    def getDropInterval(self):
        return self.dropInterval

    def getFallingDown(self):
        return self.isFallingDown
    
    def setFallingDown(self, isFallingDown):
        self.isFallingDown = isFallingDown

    def setBaseIndexes(self, baseRow, baseCol):
        for block in self.blocks:
            block.setBaseIndex(baseRow, baseCol)

    def getBlockIndexes(self):
        return [block.getIndex() for block in self.blocks]

    def getNextBlockIndexes(self):
        return [block.getNextIndex() for block in self.blocks]

    def draw(self, surface):
        for b in self.blocks:
            b.draw(surface)

    def getBlocks(self):
        return self.blocks

    def clearBlocks(self):
        self.blocks = []

    def addBlocks(self, block):
        self.blocks.append(block)

    def checkAndSetPressTime(self, key):
        ret = False
        if getCurrentTime() - self.pressTime.get(key, 0) > 150:
            ret = True
            self.pressTime[key] = getCurrentTime()
        return ret

    def keyDownHandler(self):
        pressed = pygame.key.get_pressed()
        if pressed[K_LEFT] and self.checkAndSetPressTime(K_LEFT) and not self.isPause:
            b = True
            for block in self.blocks:
                if block.isLeftBoundary():
                    b = False
                    break
            if b:
                for block in self.blocks:
                    block.moveLeft()

        if pressed[K_RIGHT] and self.checkAndSetPressTime(K_RIGHT) and not self.isPause:
            b = True
            for block in self.blocks:
                if block.isRightBoundary():
                    b = False
                    break
            if b:
                for block in self.blocks:
                    block.moveRight()

        if pressed[K_UP] and self.checkAndSetPressTime(K_UP) and not self.isPause:
            for block in self.blocks:
                block.rotate()

        if pressed[K_DOWN] and not self.isPause:
            self.setFallingDown(True)
            pygame.event.set_blocked(pygame.KEYDOWN)

        if self.blockGroupType == const.BlockGroupType.DROP:
            for block in self.blocks:
                block.setShadow(pressed[K_DOWN])

    def update(self):
        oldTime = self.dropTime
        curTime = getCurrentTime()
        diffTime = curTime - oldTime
        if self.blockGroupType == const.BlockGroupType.DROP:
            if diffTime >= self.dropInterval:
                self.dropTime = curTime
                for b in self.blocks:
                    b.drop(1)
            self.keyDownHandler()
            if self.getFallingDown():
                self.setDropInterval(30)

        for block in self.blocks:
            block.update()

        if self.getEliminate():
            if getCurrentTime() - self.eliminateTime > 500:
                tmpBlocks = []
                for block in self.blocks:
                    if block.getIndex()[0] not in self.eliminateRow:
                        if block.getIndex()[0] < self.eliminateRow[0]:
                            block.drop(len(self.eliminateRow))
                        tmpBlocks.append(block)
                self.eliminateRow.clear()
                self.blocks = tmpBlocks
                self.setEliminate(False)

    def doEliminate(self, row):
        eliminateRow = {}
        for col in range(0, const.GAME_COL):
            idx = (row, col)
            eliminateRow[idx] = 1
        self.setEliminate(True)
        self.eliminateRow.append(row)

        for block in self.blocks:
            if eliminateRow.get(block.getIndex()):
                block.startBlink()
                sound = pygame.mixer.Sound(const.ELIMINATE_SOUND)
                sound.set_volume(0.15)
                sound.play()

    def processEliminate(self):
        hash = {}

        allIndexes = self.getBlockIndexes()
        for idx in allIndexes:
            hash[idx] = 1

        eliminateRows = []
        for row in range(const.GAME_ROW - 1, -1, -1):
            full = True
            for col in range(0, const.GAME_COL):
                idx = (row, col)
                if not hash.get(idx):
                    full = False
                    break
            if full:
                eliminateRows.append(row)

        if eliminateRows:
            for row in eliminateRows:
                self.doEliminate(row)
        return len(eliminateRows)

    def setEliminate(self, bEl):
        self.eliminate = bEl
        self.eliminateTime = getCurrentTime()

    def getEliminate(self):
        return self.eliminate
