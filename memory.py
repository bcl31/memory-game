import pygame
import random


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

        self.deck = Deck(4, 4, 10, self.surface)

    def play(self):
        # Play the game until the player presses the close box.
        # - self is the Game that should be continued or not.

        while not self.close_clicked:  # until player clicks close box
            # play frame
            self.handle_events()
            self.draw()
            self.update()
            self.game_Clock.tick(self.FPS)  # run at most with FPS Frames Per Second

    def handle_events(self):
        # Handle each user event by changing the game state appropriately.
        # - self is the Game whose events will be handled

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_clicked = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.deck.click_check()

    def draw(self):
        # Draw all game objects.

        # - self is the Game to draw
        self.surface.fill(self.bg_color)  # clear the display surface first

        self.deck.draw()

        pygame.display.update()  # make the updated surface appear on the display

    def update(self):
        # Update the game objects for the next frame.
        # - self is the Game to update
        pass


class Deck:

    def __init__(self, tiles_per_row, tiles_per_column, space_between, screen):
        self.screen = screen

        # find the necessary spacing and size of the tiles relative to window size, this allows window size and
        # number of tiles to change dynamically with few issues.
        tiles_per_row += 1  # reserves a column of equal width to the rest for the score
        dimensions = list(screen.get_size())
        dimensions[1] = dimensions[1] - space_between  # this allows for spacing on bottom
        self.tile_spacing_x = dimensions[0] // tiles_per_row
        self.tile_spacing_y = dimensions[1] // tiles_per_column
        self.tile_size_x = self.tile_spacing_x - space_between
        self.tile_size_y = self.tile_spacing_y - space_between

        # create a list containing all of the names of the tile images twice, then shuffle it
        images_names = []
        for i in range(2):
            for image_num in range(1, 9):
                images_names.append('image' + str(image_num) + '.bmp')
        random.shuffle(images_names)

        # set the name for the "backside" of the tiles
        hidden_name = 'image0.bmp'

        # create one tile for each space on a grid by going through all possible x, y grid coordinate combinations
        self.deck = []

        tile_dimension = [self.tile_size_x, self.tile_size_y]
        for x in range(tiles_per_row - 1):  # the - 1 ensures tiles are not created for the column reserved for score
            for y in range(tiles_per_column):

                # find the location of the tile by multiplying the tile spacing by the grid coordinate value for
                # the respective axis by it's tile spacing, then adding the space_between to prevent tiles touching
                tile_location = [space_between + self.tile_spacing_x * x, space_between + self.tile_spacing_y * y]

                # create the tile for that spot on the grid before continuing to the next grid coordinate
                self.deck.append(tile(tile_dimension, tile_location, images_names.pop(0), hidden_name, self.screen))

    def draw(self):
        for tile in self.deck:
            tile.draw()

    def click_check(self):
        mouse_position = pygame.mouse.get_pos()
        for tile in self.deck:
            if tile.collision_check(mouse_position) and tile.check_hidden():
                tile.flip()


class tile:

    def __init__(self, dimensions, location, image, hidden_image, screen):
        self.rect = pygame.Rect(location, dimensions)
        self.color = pygame.Color('white')
        self.screen = screen
        self.hidden = True

        # retrieve images and scale them to size of tile
        front = pygame.image.load(image)
        self.front = pygame.transform.scale(front, dimensions)
        back = pygame.image.load(hidden_image)
        self.back = pygame.transform.scale(back, dimensions)

    def draw(self):
        if self.hidden:
            image = self.back
        else:  # if not self.hidden
            image = self.front
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

main()
