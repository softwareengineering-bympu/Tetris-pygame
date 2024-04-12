from blockGroup import *
import const

class Game(pygame.sprite.Sprite):
    def getRelPos(self):
        return (240, 50)

    def __init__(self, screen):
        self.font = pygame.font.Font(None, 60)
        self.score = 0
        self.screen = screen
        self.fixedBlockGroup = BlockGroup(const.BlockGroupType.FIXED, const.BLOCK_SIZE_W, const.BLOCK_SIZE_H, [], self.getRelPos())
        self.dropBlockGroup = None
        self.nextBlockGroup = None
        self.generateNextBlockGroup()
        self.gameOverImage = pygame.image.load("pic/gameover.png")
        self.isGameOver = False
        self.isPlayGameOverSound = False
        self.isPause = False
        self.pause_button_image = pygame.image.load(const.PAUSE_BUTTON_IMAGE)
        self.restart_button_image = pygame.image.load(const.RESTART_BUTTON_IMAGE)

    def getPause(self):
        return self.isPause
    
    def setPause(self, isPause):
        self.isPause = isPause

    def getGameOver(self):
        return self.isGameOver

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
        if self.isGameOver:
            return
        self.checkGameOver()

        self.fixedBlockGroup.update()

        if self.fixedBlockGroup.getEliminate():
            return

        if self.dropBlockGroup:
            self.dropBlockGroup.update()
        else:
            self.generateDropBlockGroup()
            self.dropBlockGroup.setDropInterval(900)

        if self.isCollision():
            pygame.event.set_allowed(pygame.KEYDOWN)
            self.dropBlockGroup.setFallingDown(False)
            blocks = self.dropBlockGroup.getBlocks()
            for block in blocks:
                self.fixedBlockGroup.addBlocks(block)
            self.dropBlockGroup.clearBlocks()
            self.dropBlockGroup = None
            eliminateRows = self.fixedBlockGroup.processEliminate()
            if eliminateRows > 0:
                self.score += 1 * eliminateRows

    def checkGameOver(self):
        allIndexes = self.fixedBlockGroup.getBlockIndexes()
        for index in allIndexes:
            if index[0] < 2:
                self.isGameOver = True

    def draw(self):
        self.fixedBlockGroup.draw(self.screen)
        if self.dropBlockGroup:
            self.dropBlockGroup.draw(self.screen)
        self.nextBlockGroup.draw(self.screen)

        textImage = self.font.render('Score: ' + str(self.score), True, (255,255,255))
        self.screen.blit(textImage, (10, 80))
        if self.isGameOver:
            rect = self.gameOverImage.get_rect()
            rect.centerx = const.GAME_WIDTH_SIZE / 2
            rect.centery = const.GAME_HEIGHT_SIZE / 2
            self.screen.blit(self.gameOverImage, rect)
            if not self.isPlayGameOverSound:
                sound = pygame.mixer.Sound(const.GAMEOVER_SOUND)
                sound.play()
                while pygame.mixer.get_busy():
                    pass
                self.isPlayGameOverSound = True
        
    def drawPauseSurface(self):
        pause_text = pygame.font.SysFont(None, 40).render("Game Paused", True, (255, 0, 0))
        pause_hint = pygame.font.SysFont(None, 40).render("Press ESC or the Pause to continue", True, (255, 255, 255))
        self.screen.blit(pause_text, (const.GAME_WIDTH_SIZE // 2 - pause_text.get_width() // 2,
                                      const.GAME_HEIGHT_SIZE // 2 - pause_text.get_height() // 2 - 30))
        self.screen.blit(pause_hint, (const.GAME_WIDTH_SIZE // 2 - pause_text.get_width() // 2 - 125,
                                      const.GAME_HEIGHT_SIZE // 2 - pause_text.get_height() // 2))
        
    def restart(self):
        self.fixedBlockGroup.clearBlocks()
        self.score = 0
        self.isGameOver = False
        self.isPlayGameOverSound = False
        self.generateDropBlockGroup()
        self.generateNextBlockGroup()
