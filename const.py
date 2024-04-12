import pygame

GAME_WIDTH_SIZE = 800
GAME_HEIGHT_SIZE = 600

BACKGROUND_IMAGE = "pic/background.png"
PAUSE_BUTTON_IMAGE = "pic/pause.png"
RESTART_BUTTON_IMAGE = "pic/restart.png"

# Number the color to create block in random color
class BlockType:
    RED = 0
    ORANGE = 1
    YELLOW = 2
    GREEN = 3
    CYAN = 4
    BLUE = 5
    PURPLE = 6
    BLOCKMAX = 7

class BlockGroupType:
    FIXED = 0
    DROP = 1

BLOCK_RES = {
    BlockType.RED: "pic/red.png",
    BlockType.ORANGE: "pic/orange.png",
    BlockType.YELLOW: "pic/yellow.png",
    BlockType.GREEN: "pic/green.png",
    BlockType.CYAN: "pic/cyan.png",
    BlockType.BLUE: "pic/blue.png",
    BlockType.PURPLE: "pic/purple.png",
}

ELIMINATE_SOUND = "audio/eliminate_soundeffect.mp3"
GAMEOVER_SOUND = "audio/gameover_soundeffect.mp3"

# Screen boundary
GAME_ROW = 17
GAME_COL = 10

# Set block size
BLOCK_SIZE_W = 32
BLOCK_SIZE_H = 32

BLOCK_SHAPES = [
    [((0, 0), (0, 1), (1, 0), (1, 1))],                                         # Square-Shaped
    [((0, 0), (0, 1), (0, 2), (0, 3)), ((0, 0), (1, 0), (2, 0), (3, 0))],       # Long-Shaped
    [((0, 0), (0, 1), (1, 1), (1, 2)), ((0, 1), (1, 0), (1, 1), (2, 0))],       # Left-Z-Shaped
    [((0, 2), (0, 1), (1, 1), (1, 0)), ((0, 0), (1, 0), (1, 1), (2, 1))],       # Right-Z-Shaped
    [((0, 1), (1, 0), (1, 1), (1, 2)), ((0, 1), (1, 1), (1, 2), (2, 1)),
     ((1, 0), (1, 1), (1, 2), (2, 1)), ((0, 1), (1, 0), (1, 1), (2, 1))],        # T-Shaped
    [((1, 0), (1, 1), (1, 2), (0, 0)), ((0, 1), (1, 1), (0, 2), (2, 1)),
     ((2, 2), (1, 0), (1, 1), (1, 2)), ((0, 1), (2, 0), (1, 1), (2, 1))],        # Left-L-Shaped
    [((0, 2), (1, 0), (1, 1), (1, 2)), ((0, 1), (1, 1), (2, 2), (2, 1)),
     ((1, 0), (1, 1), (1, 2), (2, 0)), ((0, 1), (0, 0), (1, 1), (2, 1))],        # Right-L-Shaped
]


