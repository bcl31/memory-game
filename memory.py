import pygame


# User-defined functions

def main():
    # initialize all pygame modules (some need initialization)
    pygame.init()
    # create a pygame display window
    pygame.display.set_mode((500, 400))
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

    def draw(self):
        # Draw all game objects.
        self.deck.draw()
        # - self is the Game to draw
        self.surface.fill(self.bg_color)  # clear the display surface first
        pygame.display.update()  # make the updated surface appear on the display

    def update(self):
        # Update the game objects for the next frame.
        # - self is the Game to update
        pass


class Deck:

    def __init__(self, cards_per_row, cards_per_column, space_between, screen):
        dimensions = list(screen.get_size())
        dimensions[0] = dimensions[0] - 100  # this allows space for score on right
        self.card_spacing_x = dimensions[0] // cards_per_row
        self.card_spacing_y = dimensions[1] // cards_per_column
        self.card_size_x = self.card_spacing_x - space_between
        self.card_size_y = self.card_spacing_y - space_between
        self.deck = []
        self.screen = self.screen
        for x in range(cards_per_row):
            for y in range(cards_per_column):
                card_dimension = [self.card_size_x, self.card_size_y]
                card_location = [space_between + self.card_spacing_x * x, space_between + self.card_spacing_y * y]
                self.deck.append(Card(card_dimension, card_location, None, screen))

    def draw(self):
        for card in self.deck:
            card.draw()


class Card:

    def __init__(self, dimensions, location, image, screen):
        self.rect = pygame.Rect(location, dimensions)
        self.color = pygame.Color('white')
        self.screen = screen

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)


main()
