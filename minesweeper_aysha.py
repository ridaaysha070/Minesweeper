import pygame
import random
from pygame import mixer
import os
pygame.init()
mixer.init()

s = 'Sprites'

bomb = pygame.mixer.Sound(os.path.join(s, 'explosion.mp3'))
win = pygame.mixer.Sound(os.path.join(s, 'win.wav'))

bg_color = (103, 124, 138)
grid_color = (128, 128, 128)

game_width = 15
game_height = 15
numMine = 14
grid_size = 32  # Size of grid change the image dimension if this is changed)
border = 16  # Top border
top_border = 100  # Left, Right, Bottom border
display_width = grid_size * game_width + border * 2  # Display width
display_height = grid_size * game_height + border + top_border  # Display height
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Minesweeper by Thrysha")



# Import images
spr_emptyGrid = pygame.image.load("Sprites/empty.png")
spr_flag = pygame.image.load("Sprites/flag.png")
spr_grid = pygame.image.load("Sprites/Grid.png")
spr_grid1 = pygame.image.load("Sprites/grid1.png")
spr_grid2 = pygame.image.load("Sprites/grid2.png")
spr_grid3 = pygame.image.load("Sprites/grid3.png")
spr_grid4 = pygame.image.load("Sprites/grid4.png")
spr_grid5 = pygame.image.load("Sprites/grid5.png")

spr_mine = pygame.image.load("Sprites/mine.png")
spr_mineClicked = pygame.image.load("Sprites/mineClicked.png")
spr_mineFalse = pygame.image.load("Sprites/mineFalse.png")


grid = []  # The main grid
mines = []  # Pos of the mines


# Create funtion to draw texts
def drawText(txt, s, yOff=0):
    screen_text = pygame.font.SysFont("Cambria", s, True).render(txt, True, (0, 0, 0))
    rect = screen_text.get_rect()
    rect.center = (game_width * grid_size / 2 + border, game_height * grid_size / 2 + top_border + yOff)
    gameDisplay.blit(screen_text, rect)


# Create class grid
class Grid:
    def __init__(self, xGrid, yGrid, type):
        self.xGrid = xGrid  # X pos of grid
        self.yGrid = yGrid  # Y pos of grid
        self.clicked = False  # Boolean var to check if the grid has been clicked
        self.mineClicked = False  # Bool var to check if the grid is clicked and its a mine
        self.mineFalse = False  # Bool var to check if the player flagged the wrong grid
        self.flag = False  # Bool var to check if player flagged the grid
        # Create rectObject to handle drawing and collisions
        self.rect = pygame.Rect(border + self.xGrid * grid_size, top_border + self.yGrid * grid_size, grid_size, grid_size)
        self.val = type  # Value of the grid, -1 is mine

    def drawGrid(self):
        # Draw the grid according to bool variables and value of grid
        if self.mineFalse:
            gameDisplay.blit(spr_mineFalse, self.rect)
        else:
            if self.clicked:
                if self.val == -1:
                    if self.mineClicked:
                        gameDisplay.blit(spr_mineClicked, self.rect)
                    else:
                        gameDisplay.blit(spr_mine, self.rect)
                else:
                    if self.val == 0:
                        gameDisplay.blit(spr_emptyGrid, self.rect)
                    elif self.val == 1:
                        gameDisplay.blit(spr_grid1, self.rect)
                    elif self.val == 2:
                        gameDisplay.blit(spr_grid2, self.rect)
                    elif self.val == 3:
                        gameDisplay.blit(spr_grid3, self.rect)
                    elif self.val == 4:
                        gameDisplay.blit(spr_grid4, self.rect)
                    elif self.val == 5:
                        gameDisplay.blit(spr_grid5, self.rect)

            else:
                if self.flag:
                    gameDisplay.blit(spr_flag, self.rect)
                else:
                    gameDisplay.blit(spr_grid, self.rect)

    def revealGrid(self):
        self.clicked = True
        # Auto reveal if it's a 0
        if self.val == 0:
            for x in range(-1, 2):
                if self.xGrid + x >= 0 and self.xGrid + x < game_width:
                    for y in range(-1, 2):
                        if self.yGrid + y >= 0 and self.yGrid + y < game_height:
                            if not grid[self.yGrid + y][self.xGrid + x].clicked:
                                grid[self.yGrid + y][self.xGrid + x].revealGrid()
        elif self.val == -1:
            # Auto reveal all mines if it's a mine
            for m in mines:
                if not grid[m[1]][m[0]].clicked:
                    grid[m[1]][m[0]].revealGrid()

    def updateValue(self):
        # Update the value when all grid is generated
        if self.val != -1:
            for x in range(-1, 2):
                if self.xGrid + x >= 0 and self.xGrid + x < game_width:
                    for y in range(-1, 2):
                        if self.yGrid + y >= 0 and self.yGrid + y < game_height:
                            if grid[self.yGrid + y][self.xGrid + x].val == -1:
                                self.val += 1


def gameLoop():
    gameState = "Playing"  # Game state
    mineLeft = numMine  # Number of mine left
    global grid  # Access global var
    grid = []
    global mines
    t = 0  # Set time to 0

    # Generating mines
    mines = [[random.randrange(0, game_width),
              random.randrange(0, game_height)]]

    for c in range(numMine - 1):
        pos = [random.randrange(0, game_width),
               random.randrange(0, game_height)]
        same = True
        while same:
            for i in range(len(mines)):
                if pos == mines[i]:
                    pos = [random.randrange(0, game_width), random.randrange(0, game_height)]
                    break
                if i == len(mines) - 1:
                    same = False
        mines.append(pos)

    # Generating entire grid
    for j in range(game_height):
        line = []
        for i in range(game_width):
            if [i, j] in mines:
                line.append(Grid(i, j, -1))
            else:
                line.append(Grid(i, j, 0))
        grid.append(line)

    # Update of the grid
    for i in grid:
        for j in i:
            j.updateValue()

    # Main Loop
    while gameState != "Exit":
        # Reset screen
        gameDisplay.fill(bg_color)

        # User inputs
        for event in pygame.event.get():
            # Check if player close window
            if event.type == pygame.QUIT:
                gameState = "Exit"
            # Check if play restart
            if gameState == "Game Over" or gameState == "Win":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        gameState = "Exit"
                        gameLoop()
            else:
                if event.type == pygame.MOUSEBUTTONUP:
                    for i in grid:
                        for j in i:
                            if j.rect.collidepoint(event.pos):
                                if event.button == 1:
                                    # If player left clicked of the grid
                                    j.revealGrid()
                                    # Toggle flag off
                                    if j.flag:
                                        mineLeft += 1
                                        j.falg = False
                                    # If it's a mine
                                    if j.val == -1:
                                        gameState = "Game Over"
                                        j.mineClicked = True
                                elif event.button == 3:
                                    # If the player right clicked
                                    if not j.clicked:
                                        if j.flag:
                                            j.flag = False
                                            mineLeft += 1
                                        else:
                                            j.flag = True
                                            mineLeft -= 1

        # Check if won
        w = True
        for i in grid:
            for j in i:
                j.drawGrid()
                if j.val != -1 and not j.clicked:
                    w = False
        if w and gameState != "Exit":
            gameState = "Win"

        # Draw texts when game ends
        if gameState != "Game Over" and gameState != "Win":
            t += 1
        elif gameState == "Game Over":
            drawText("Game Over!", 50)
            drawText("press space to restart", 35, 50)
            pygame.mixer.Sound.play(bomb)

            for i in grid:
                for j in i:
                    if j.flag and j.val != -1:
                        j.mineFalse = True
        else:
            pygame.mixer.Sound.play(win)
            drawText("You WON!", 50)
            drawText("press space to restart", 35, 50)

        # Draw the mines that are left
        screen_text = pygame.font.SysFont("Cambria", 50).render(mineLeft.__str__(), True, (0, 0, 0))
        gameDisplay.blit(screen_text, (display_width/2 - 25, border))

        pygame.display.update()

gameLoop()
pygame.quit()
quit()
