import pygame, sys
from pygame.locals import *
from blockGroup import *
import const

class Game(pygame.sprite.Sprite):
    def getRelPos(self):
        return (240, 50)

    def __init__(self, screen):
        self.font = pygame.font.Font(None, 60)
        self.score = 0
        self.screen = screen
        self.isGameOver = False
        self.fixedBlockGroup = BlockGroup(const.BlockGroupType.FIXED, const.BLOCK_SIZE_W, const.BLOCK_SIZE_H, [], self.getRelPos())
        self.dropBlockGroup = None
        self.nextBlockGroup = None
        self.generateNextBlockGroup()

    def generateDropBlockGroup(self):
        self.dropBlockGroup = self.nextBlockGroup
        self.dropBlockGroup.setBaseIndexes(0, const.GAME_COL/2-1)
        self.generateNextBlockGroup()
    
    def generateNextBlockGroup(self):
        conf = BlockGroup.GenerateBlockGroupConfig(0, const.GAME_COL + 3)
        self.nextBlockGroup = BlockGroup(const.BlockGroupType.DROP, const.BLOCK_SIZE_W, const.BLOCK_SIZE_H, conf, self.getRelPos())

    def isCollision(self):
        hash = {}
        allIndexes = self.fixedBlockGroup.getBlockIndexes()
        for idx in allIndexes:
            hash[idx] = 1
        dropIndexes = self.dropBlockGroup.getNextBlockIndexes()

        for dropIndex in dropIndexes:
            if hash.get(dropIndex):
                return True
            if dropIndex[0] >= const.GAME_ROW:
                return True
        return False


    def update(self):
        self.fixedBlockGroup.update()

        if self.fixedBlockGroup.getEliminate():
            return

        if self.dropBlockGroup:
            self.dropBlockGroup.update()
        else:
            self.generateDropBlockGroup()

        if self.isCollision():
            blocks = self.dropBlockGroup.getBlocks()
            for block in blocks:
                self.fixedBlockGroup.addBlocks(block)
            self.dropBlockGroup.clearBlocks()
            self.dropBlockGroup = None
            eliminateRows = self.fixedBlockGroup.processEliminate()
            if eliminateRows > 0:
                self.score += 1 * eliminateRows

    def draw(self):
        self.fixedBlockGroup.draw(self.screen)
        if self.dropBlockGroup:
            self.dropBlockGroup.draw(self.screen)
        self.nextBlockGroup.draw(self.screen)


        textImage = self.font.render('Score: ' + str(self.score), True, (255,255,255))
        self.screen.blit(textImage, (10, 20))