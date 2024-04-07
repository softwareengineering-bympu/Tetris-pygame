import pygame, sys
from pygame.locals import *
import const
from game import Game
def main():
    pygame.init()
    background = pygame.image.load(const.BACKGROUND_IMAGE)
    DISPLAYSURF = pygame.display.set_mode((const.GAME_WIDTH_SIZE, const.GAME_HEIGHT_SIZE))
    game = Game(DISPLAYSURF)

    # pause and restart button set
    pause_button_rect = pygame.Rect(10, 10, 80, 80)
    pause_button_image = pygame.image.load(const.PAUSE_BUTTON_IMAGE)
    restart_button_rect = pygame.Rect(300, 300, 200, 124)
    restart_button_image = pygame.image.load(const.RESTART_BUTTON_IMAGE)

    # pause boolean
    is_paused = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # pause control
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    is_paused = not is_paused

            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if pause_button_rect.collidepoint(event.pos):
                    is_paused = not is_paused
                if restart_button_rect.collidepoint(event.pos):
                    main()

        # pause hint surface
        if is_paused:
            game.drawPauseSurface()
            DISPLAYSURF.blit(restart_button_image, (restart_button_rect.x + 10, restart_button_rect.y + 10))

        else:
            # common logic
            game.update()
            DISPLAYSURF.fill((0, 0, 0))
            DISPLAYSURF.blit(background, (0, 0))
            game.draw()
            if game.getGameOver():
                DISPLAYSURF.blit(restart_button_image, (restart_button_rect.x + 10, restart_button_rect.y + 30))

            DISPLAYSURF.blit(pause_button_image, (pause_button_rect.x + 10, pause_button_rect.y + 10))

        pygame.display.update()


if __name__ == '__main__':
    main()
