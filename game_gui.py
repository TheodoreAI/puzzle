# Mateo Estrada
# March, 2021
# CS325
# portfolio project

# The following is my rendition of the 8-puzzle using the following algorithms:
# the following implementation of a GUI for a sliding puzzle was taken from: https://github.com/lvidarte/sliding-puzzle/blob/master/puzzle.py
# I modified it to be able to insert values into the puzzle and added a lot of different functionalities.


import pygame
import os
import sys
import random


from algorithm import Solution


class Error(Exception):
    pass


class InputError(Error):
    """If there isn't the right number of inputs it will not like it!"""

    def __init__(self, msg):
        self.msg = msg


# accepts the values from the terminal
# arr_input = sys.argv[1]
#
# # removes the commas
# arr_input = arr_input.split(',')
#
# # turns it into an array of ints
# int_arr = []
# for i in arr_input:
#     int_arr.append(int(i))
#
# if len(int_arr) != 9:
#     raise InputError("The input values have to be 9 where 0 is the 'blank' space.")


# checks the input starting point to see if it can be solved.
# solutions = Solution(int_arr)
# solutions.checkSolution()
#

# this one works: python game_gui.py 0,1,3,4,2,5,7,8,6

# this one you can't solve: python game_gui.py 1,2,3,4,5,6,8,7,0

# The following code was taken from: https://www.youtube.com/watch?v=afC3dq9MeJg this tutorial. It was modified to meet the requirments of assignmnet.


class App:
    # needs three arguments
    # grid size, size of tiles and the size of the margin size, the input_arr will start the puzzle
    def __init__(self, grid_size, tile_size, margin_size, screen):
        self.grid_size = grid_size
        self.tile_size = tile_size
        self.margin_size = margin_size
        self.screen = screen
        self.prev_pos = None

        # self.input_arr = sys.argv[1].split(',')

        # the tiles go here:
        self.tiles_len = grid_size[0] * grid_size[1] - 1  # I only need the first 8

        self.tiles = [(x, y) for y in range(grid_size[1]) for x in
                      range(grid_size[0])]  # builds the grid except the blank
        # this builds the tiles using the tile size and the margin size attribute

        self.tile_pos = {(x, y): (x * (tile_size + margin_size), y * (tile_size + margin_size) + margin_size) for y in
                         range(grid_size[1]) for x in range(grid_size[0])}

        # Now I will build the font that goes into the puzzle, this font will also be insertable via the command line:

        self.font = pygame.font.Font(None, 120)

        #     this will make the images and center them:

        self.images = []

        #  this Is where I fill our the tiles with the values inserted from the terminal
        for i in range(self.tiles_len):
            image = pygame.Surface((tile_size, tile_size))
            image.fill((0, 255, 0))

            # important part here
            text = self.font.render(str(i + 1), 2, (0, 0, 0))
            w, h = text.get_size()

            # centering the values in the tile
            image.blit(text, ((tile_size - w) / 2, (tile_size - h) / 2))

            self.images += [image]

    def getOpenTile(self):
        """This is the tile that is going to be blank"""

        return self.tiles[-1]

    def setBlank(self, pos):
        self.tiles[-1] = pos

    blank_tile = property(getOpenTile, setBlank)

    def slide(self, tile):

        """This is going to move the tiles"""

        self.tiles[self.tiles.index(tile)], self.blank_tile, self.prev_pos = self.blank_tile, tile, self.blank_tile

        self.check_state(self.tiles)

    def in_grid(self, tile):
        """checks if its on the grid"""

        return tile[0] >= 0 and tile[0] < self.grid_size[0] and tile[1] >= 0 and tile[1] < self.grid_size[1]

    def check_adj(self):
        """this checks if the tile movements are adjacent"""
        # Most important rule
        x, y = self.blank_tile
        return (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)


    def randomize(self):
        """This function sets the puzzle to some random state that falls within the rules of the game:"""
        # this will call the adk_ rules

        # creates an adjacent() function object
        adjacent = self.check_adj()

        # makes an array from the position of the tiles in the grid
        adjacent = [pos for pos in adjacent if self.in_grid(pos) and pos!= self.prev_pos]

        # gets the tiles to be randomized
        tile = random.choice(adjacent)

        # slides the tiles to that random choice
        if tile != self.prev_pos:
            self.slide(tile)







    def update(self, dt):
        """This will find the tile the mouse is on if held, switch, as long as the blank is adjacent"""
        mouse = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        #     I can start by checking
        if mouse[0]:

            # solving the problem of clicking near the margin of the tiles

            x, y = mouse_pos[0] % (self.tile_size + self.margin_size), mouse_pos[1] % (
                    self.tile_size + self.margin_size)

            if x > self.margin_size and y > self.margin_size:

                tile = mouse_pos[0] // self.tile_size, mouse_pos[1] // self.tile_size
                if self.in_grid(tile):
                    if tile in self.check_adj():
                        # if the tile is in the grid then set it to be able to move it
                        # if the tile checks out the adjacent rule then it gets to slide
                        self.slide(tile)

    def draw(self, screen):
        """This is where I will insert the values that are inputted by the user!"""

        for i in range(self.tiles_len):
            x, y = self.tile_pos[self.tiles[i]]
            screen.blit(self.images[i], (x, y))

    def check_state(self, tile_position):
        """This checks if the tiles are in a won state"""

        # if tile arragement is [1,2,3,4,5,6,7,8, blank]
        # return true
        # else
        # you haven't won yet!
        won_state = [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)]

        if tile_position == won_state:
            # print("You have won!", tile_position)
            self.display_state(True)



        elif tile_position != won_state:
            self.display_state(False)
            # print("You haven't won yet!", tile_position)

    def display_state(self, state):
        """This will display a message on the board"""
        #
        # pygame.font.init()
        # my_font = pygame.font.SysFont('Comic Sans MS', 30, 'White')
        #
        # text_surface = my_font.render('You have won!', False, (0, 0, 0))
        if state:
            pygame.display.set_caption("You have won!")
        else:
            pygame.display.set_caption("8-Puzzle (Sliding Puzzle)")


    def events(self, event):
        """This checks to see if the users made a move"""

        count = 0
        saved_states = []

        # check if there was a key pressed
        if event.type == pygame.KEYDOWN:

            # if the spacebar is hit then randomize!

            if event.key == pygame.K_SPACE:
                # this loop makes the randomize() function run 10 times.
                for i in range(200000):

                    copy_grid = self.tiles
                    count +=1
                    if self.tiles not in saved_states:
                        saved_states.append(list(copy_grid))

                    # if the pattern of the tiles is not in the saved states array, then save it and count it
                    self.randomize()

                self.save_states(count, saved_states)







    def save_states(self, count, saved_states):
        """This function gets called to save the states of the game:"""

        check = True
        count_not_equal = 0
        print(count, len(saved_states))





    # def breath_first_search(self, root):
    #     """This searches the best path to a solution."""
    #
    #     open_list = []
    #
    #     visited_nodes = set()
    #
    #     open_list.append(root)
    #     visited.add(tuple(root.puzzle))
    #
    #     while(True):
    #         current_node = open_list.pop(0)
    #         if current_node.goaltest()
    #



def main():
    """Pygame window positioning, initialization, and captions were used in accordance to this resource: https://www.pygame.org/wiki/FrequentlyAskedQuestions"""
    pygame.init()
    position = 100, 100
    os.environ['SDL_VIDEO_WINDOW_POS'] = str(position[0]) + "," + str(position[1])

    pygame.display.set_caption("8-puzzle (Sliding Puzzle)")
    # pygame.display.set_caption("In order to win you must place the values in ascending order:")
    screen = pygame.display.set_mode((800, 600))

    fpsclock = pygame.time.Clock()

    # this is what starts the application:
    # takes the grid_size, the tile_size, and the margin_size, and the screen object
    program = App((3, 3), 100, 5, screen)

    while True:
        dt = fpsclock.tick() / 1000

        screen.fill((0, 0, 0))
        program.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # if I click the space key then execute this
            program.events(event)

        program.update(dt)


if __name__ == '__main__':
    main()
