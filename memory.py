# this program is a simple matching game, in the top left a timer increases until all tiles have been matched.
# if an incorrect match was made, the game will freeze for a one second penalty before hiding the tiles again
# tiles are selected by clicking on them, at which point they will be revealed

import pygame
import random
import time


# User-defined functions

def main():
    # initialize all pygame modules (some need initialization)
    pygame.init()
    # create a pygame display window
    pygame.display.set_mode((1000, 800))  # works best with tiles_per_row + 1 : tiles_per_column aspect ratio (5:4)
    # set the title of the display window
    pygame.display.set_caption('Memory')
    # get the display surface
    w_surface = pygame.display.get_surface()
    # create a game object
    game = Game(w_surface)
    # start the main game loop by calling the play method on the game object
    game.play()
    # quit pygame and clean up the pygame window
    pygame.quit()


# User-defined classes
# tracks general gameplay specific features
class Game:
    # An object in this class represents a complete game.

    def __init__(self, surface):
        # Initialize a Game.
        # - self is the Game to initialize
        # - surface is the display window surface object

        # === objects that are part of every game that we will discuss
        self.surface = surface
        self.bg_color = pygame.Color('black')

        self.FPS = 60
        self.game_Clock = pygame.time.Clock()
        self.close_clicked = False
        self.continue_game = True

        # === objects that are only a part of memory

        # --- Clock
        self.clock = clock_render()

        # --- Tiles

        # find the spacing between tile coordinates needed
        tiles_per_row = 4
        tiles_per_column = 4
        spacing = 10
        space_between_tiles = find_tile_spacing(tiles_per_row, tiles_per_column, spacing, self.surface)

        # find the size of tiles needed
        tile_dimension = [space_between_tiles[0] - spacing, space_between_tiles[1] - spacing]

        # create a list containing the names of the image files for all cards twice, as well as hidden image
        image_names = image_list_shuffled()
        hidden_name = "image0.bmp"

        # create all the tiles, and store them in a list

        # create one tile for each space on a grid by going through all possible x, y grid coordinate combinations
        self.deck = []

        for x in range(tiles_per_row):
            for y in range(tiles_per_column):

                # find the location of the tile by multiplying the tile spacing by the grid coordinate value for
                # the respective axis by it's tile spacing, then adding the space_between to prevent tiles touching
                tile_location = [spacing + space_between_tiles[0] * x, spacing + space_between_tiles[1] * y]

                # create the tile for that spot on the grid before continuing to the next grid coordinate
                self.deck.append(Tile(tile_dimension, tile_location, image_names.pop(0), hidden_name, self.surface))

        # create an attribute to track tiles currently 'active' (not covered and not matched)
        self.active_tiles = []

    # this method handles the loop of all processes that occur every frame
    def play(self):
        # Play the game until the player presses the close box.
        # - self is the Game that should be continued or not.

        while not self.close_clicked:  # until player clicks close box
            # play frame
            self.handle_events()
            self.draw()

            # if all tiles have not yet been revealed
            if self.continue_game:
                self.update()
                self.decide_continue()
            self.game_Clock.tick(self.FPS)  # run at most with FPS Frames Per Second

    # this method handles all action related to user input
    def handle_events(self):
        # get all inputs that have occurred since last check
        events = pygame.event.get()
        for event in events:

            # if the event was an attempt to close the game, flag the game to be closed
            if event.type == pygame.QUIT:
                self.close_clicked = True

            # if the event was a mouse click, check if a tile was clicked on and which one
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.click_check()

    # this method is responsible for drawing all graphical elements to the screen
    def draw(self):

        self.surface.fill(self.bg_color)  # clear the display surface first

        # draw tiles to screen
        for tile in self.deck:
            tile.draw()

        # draw clock to screen
        self.surface.blit(self.clock, (self.surface.get_size()[0] - self.clock.get_size()[0], 0))

        pygame.display.update()  # make the updated surface appear on the display

    # this method is responsible for updating all game objects that are not influenced directly by the player
    def update(self):

        # check if active cards are matching
        self.match_check()

        # update the clock
        self.clock = clock_render()

    # this method checks if the active cards are matching, if not, it waits one second before hiding them again
    def match_check(self):
        # check if more than one card is active, if so, check if they match
        if len(self.active_tiles) > 1:
            tile1, tile2 = self.active_tiles
            pair = tile1.pair_check(tile2)

            # if the tiles do not match, flip them over again and wait a 1 second penalty
            if not pair:
                tile1.flip()
                tile2.flip()
                time.sleep(1)

            # clear the tiles from the active tile list regardless
            self.active_tiles = []

    # this method is responsible for checking if the game has come to an end, if so, it marks continue_game as False
    def decide_continue(self):

        # check if any tiles are still hidden
        uncovered = []
        for tile in self.deck:
            if tile.check_hidden():
                uncovered.append(tile)

        # if no tiles are still hidden, all tiles must be matched, therefore the game is over
        if len(uncovered) <= 0:
            self.continue_game = False

    # this method should only be called when a mouse down event is detected. when called, it checks if the mouse
    # position is currently over any of the tiles, if so, it flips the tile and adds it to the active tile list
    def click_check(self):
        # check if mouse is colliding with any hidden tiles
        mouse_position = pygame.mouse.get_pos()
        for tile in self.deck:
            if tile.collision_check(mouse_position) and tile.check_hidden():
                # if so, flip tile and mark it as active
                tile.flip()
                self.active_tiles.append(tile)


# this class represents one tile in the memory game
# a tile has a front and a back side
# a tile can either be face up or face down
# a tile displays the side that is currently up
# a tile is a rectangle of a specified size
# a tile is located at a specific location on the screen
class Tile:

    # dimensions is a list containing the dimensions of the tile in [width, height] format
    # location is a list containing the coordinates for the top left corner of the tile in [x, y] format
    # image is a string containing the name of the image file for the front side of the tile
    # hidden_image is a string containing the name of the image file for the back side of the tile
    # screen is the surface the tile will be drawn to
    def __init__(self, dimensions, location, image, hidden_image, screen):
        self.rect = pygame.Rect(location, dimensions)
        self.screen = screen
        self.hidden = True
        self.front_id = image

        # retrieve images and scale them to size of tile
        front = pygame.image.load(image)
        self.front = pygame.transform.scale(front, dimensions)
        back = pygame.image.load(hidden_image)
        self.back = pygame.transform.scale(back, dimensions)

    # this method is responsible for drawing the tile to the screen
    def draw(self):
        # if the tile is hidden (face-down) set the image to the backside, otherwise set the image to the front side
        if self.hidden:
            image = self.back
        else:  # if not self.hidden
            image = self.front

        # print the decided image to the screen at the location of the tile's rect
        self.screen.blit(image, self.rect)

    # pos is a list or tuple containing coordinates

    # this method checks if the coordinates provided are in collision with the tile, if so, it returns true, else false
    def collision_check(self, pos):
        return self.rect.collidepoint(pos[0], pos[1])

    # this method, when called, toggles whether or not the tile is hidden
    def flip(self):
        self.hidden = not self.hidden

    # this method returns a boolean indicating if the tile is hidden (True) or revealed (False)
    def check_hidden(self):
        return self.hidden

    # this method returns the name of the image shown on the front of the card
    def get_image_name(self):
        return self.front_id

    # tile is an object containing information about the tile this tile is being checked against

    # this method checks if the tile provided to it has the same image as itself. if so, it returns True, else False
    def pair_check(self, tile):
        other_name = tile.get_image_name()
        this_name = self.front_id
        if this_name == other_name:
            match = True
        else:  # if this_name != other_name
            match = False
        return match


# this function creates a shuffled list containing the names for all the front tile images twice
def image_list_shuffled():
    # create a list containing all of the names of the tile images twice, then shuffle it
    images_names = []
    for i in range(2):
        for image_num in range(1, 9):
            images_names.append('image' + str(image_num) + '.bmp')
    random.shuffle(images_names)
    return images_names


# tiles_per_row is an int containing the number of tiles that have to fit horizontally across the screen
# tiles_per_column is an int containing the number of tiles that have to fit vertically stacked on the screen
# space between is an int containing the size of the border between cards, in pixels
# screen is the surface the tile will later be printed to

# this function finds the necessary spacing between tile items coordinates in order to fit properly within the window
# it returns a list containing the necessary spacing in [x, y] format
def find_tile_spacing(tiles_per_row, tiles_per_column, space_between, screen):
    tiles_per_row += 1  # reserves a column of equal width to the rest for the score
    dimensions = list(screen.get_size())
    dimensions[1] = dimensions[1] - space_between  # this allows for spacing on bottom
    tile_spacing = [0, 0]  # needed to establish size of list, values here are irrelevant
    tile_spacing[0] = dimensions[0] // tiles_per_row
    tile_spacing[1] = dimensions[1] // tiles_per_column
    return tile_spacing


# this method creates a surface containing a number indicating the amount of seconds since the game started
def clock_render():
    # Text settings
    font_size = 60
    font = pygame.font.SysFont("arial", font_size)
    color = pygame.Color("white")

    # render the clock
    game_time = pygame.time.get_ticks()
    game_time = game_time / 1000
    game_time = int(round(game_time, 0))  # round to whole number
    game_time = str(game_time)
    clock = pygame.font.Font.render(font, game_time, True, color)
    return clock


main()
