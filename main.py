import pygame, sys
from pygame.locals import *
import const
from game import Game

pygame.init()
background = pygame.image.load(const.BACKGROUND_IMAGE)
DISPLAYSURF = pygame.display.set_mode((const.GAME_WIDTH_SIZE, const.GAME_HEIGHT_SIZE))
game = Game(DISPLAYSURF)

while True:
    for event in pygame.event.get():
        # every control in the event
        game.quitControl(event)
        game.pauseControl(event)
        game.startControl(event)
        game.backStartControl(event)
        game.restartControl(event)

    if game.getStart():
        # draw the cover
        game.drawStartSurface()

    else:
        # pause hint surface
        if game.getPause():
            game.drawPauseSurface()
                
        else:
            # common logic
            game.update()
            DISPLAYSURF.fill((0, 0, 0))
            DISPLAYSURF.blit(background, (0, 0))
            game.drawMain()
            if game.getGameOver():
                game.drawGameOverImage()
                game.drawRestartButton(330, 400)
                game.playGameOverSound()
            else:
                game.drawPauseButton()

    pygame.display.update()