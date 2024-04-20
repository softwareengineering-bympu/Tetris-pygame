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
        if isFallingDown:
            pygame.key.set_mods(KMOD_MODE)
        else:
            pygame.key.set_mods(0)

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

    def rotate(self):
        # Try to rotate
        for block in self.blocks:
            block.rotate()

        # Check whether the left boundary has been crossed
        leftOffsets = [block.colIdx for block in self.blocks if block.colIdx < 0]
        if leftOffsets:
            minLeftOffset = min(leftOffsets)
            # If cross the left boundary, move all blocks to the right
            for block in self.blocks:
                block.moveRight(abs(minLeftOffset))

        # Check whether the right boundary has been crossed
        rightOffsets = [block.colIdx - (const.GAME_COL - 1) for block in self.blocks if block.colIdx >= const.GAME_COL]
        if rightOffsets:  # 如果列表不为空
            maxRightOffset = max(rightOffsets)
            # If cross the right boundary, move all blocks to the left
            for block in self.blocks:
                block.moveLeft(maxRightOffset)

    def isPositionOccupied(self, row, col, fixedBlockGroup):
        # 检查给定位置是否被静止的方块组占据
        for block in fixedBlockGroup.getBlocks():
            if (block.rowIdx, block.colIdx) == (row, col):
                return True
        return False

    def canMove(self, direction, fixedBlockGroup):
        # 检查是否可以向指定方向移动
        for block in self.blocks:
            nextRow, nextCol = block.rowIdx, block.colIdx
            if direction == "left":
                nextCol -= 1
            elif direction == "right":
                nextCol += 1
            if nextCol < 0 or nextCol >= const.GAME_COL or self.isPositionOccupied(nextRow, nextCol, fixedBlockGroup):
                return False
        return True

    def keyDownHandler(self, fixedBlockGroup):
        pressed = pygame.key.get_pressed()
        if pressed[K_LEFT] and self.checkAndSetPressTime(K_LEFT) and not self.isPause:
            if self.canMove("left", fixedBlockGroup):
                for block in self.blocks:
                    block.moveLeft(1)

        if pressed[K_RIGHT] and self.checkAndSetPressTime(K_RIGHT) and not self.isPause:
            if self.canMove("right", fixedBlockGroup):
                for block in self.blocks:
                    block.moveRight(1)

        if pressed[K_UP] and self.checkAndSetPressTime(K_UP) and not self.isPause:
            self.rotate()

        if pressed[K_DOWN] and self.checkAndSetPressTime(K_DOWN) and not self.isPause:
            self.setFallingDown(True)

        if self.blockGroupType == const.BlockGroupType.DROP:
            for block in self.blocks:
                block.setShadow(pressed[K_DOWN])

    def update(self, fixedBlockGroup=None):
        oldTime = self.dropTime
        curTime = getCurrentTime()
        diffTime = curTime - oldTime
        if self.blockGroupType == const.BlockGroupType.DROP:
            if diffTime >= self.dropInterval:
                self.dropTime = curTime
                for b in self.blocks:
                    b.drop(1)
            if fixedBlockGroup is not None:
                self.keyDownHandler(fixedBlockGroup)
            if self.getFallingDown():
                self.setDropInterval(30)

        for block in self.blocks:
            block.update()

        if self.getEliminate():
            if getCurrentTime() - self.eliminateTime > 500:
                tmpBlocks = []
                for block in self.blocks:
                    if block.getIndex()[0] not in self.eliminateRow:
                        
                        # if the current block is between the first and second row of blocks should be eliminated
                        if len(self.eliminateRow) > 1 and block.getIndex()[0] < self.eliminateRow[0] and block.getIndex()[0] > self.eliminateRow[1]:
                            block.drop(1)
                        # if the current block is between the second and third blocks should be eliminated
                        elif len(self.eliminateRow) > 2 and block.getIndex()[0] < self.eliminateRow[1] and block.getIndex()[0] > self.eliminateRow[2]:
                            block.drop(2)

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
        sound.set_volume(0.2)
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