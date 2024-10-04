from typing import List
from ut import Vec2D, print_dict_map, dict_map_to_list
from copy import deepcopy
import matplotlib.pyplot as plt
import random

class Crossword:
    def __init__(self, words: List[str]):
        self.grid = {}
        # Generate the grid
        for word in words: 
            self.place_word(word=word)

    def get_overlaps(self):
        return sum(1 for pos in self.grid.keys() for neighbor in pos.neighbors_orthogonal() if not self.grid.get(neighbor, '') == '')

    def can_place(self, char: str, pos: Vec2D, overlap: Vec2D):

        if pos == overlap: return True

        if self.grid.get(pos, '') not in ['', char]:
            return False 
        
        for neighbour in pos.neighbors_orthogonal():
            if neighbour == overlap: continue
            if not self.grid.get(neighbour, '') == '': return False

        return True

    def try_place_word(self, word: str, pos: Vec2D, word_i: int):

        # Try Horizontal 

        new_grid = deepcopy(self.grid)
        
        for char_i, char in enumerate(word):
            char_pos = pos + Vec2D(0, (char_i - word_i))
            if self.can_place(char=char, pos=char_pos, overlap=pos):
                new_grid[char_pos] = char
            else:
                break
        else:
            self.grid = new_grid
            return True

        # Try Vertical

        new_grid = deepcopy(self.grid)

        for char_i, char in enumerate(word):
            char_pos = pos + Vec2D((char_i - word_i), 0)
            if self.can_place(char=char, pos=char_pos, overlap=pos):
                new_grid[char_pos] = char
            else:
                break
        else:
            self.grid = new_grid
            return True

        return False

    def place_word(self, word: str):

        items_list = list(self.grid.items())
        random.shuffle(items_list)

        word_list = list(enumerate(word))
        random.shuffle(word_list)

        for word_i, new_char in word_list:
            for pos, char in items_list:
                if new_char == char:
                    if self.try_place_word(word=word, pos=pos, word_i=word_i):
                        return

        if self.grid == {}:
            self.try_place_word(word=word, pos=Vec2D(0, 0), word_i=0)

    

    def plot_crossword(self):

        
        xs = [pos.x for pos in self.grid.keys()]
        ys = [pos.y for pos in self.grid.keys()]
        max_x, min_x = max(xs), min(xs)
        max_y, min_y = max(ys), min(ys)

        word_index = 1

        rows = max_x - min_x + 1
        cols = max_y - min_y + 1  

        # Define the letters for the grid (with empty spaces for blacked-out cells)
        letters = dict_map_to_list(self.grid)

        # Create the plot
        fig, ax = plt.subplots(figsize=(50, 50))

        # Hide axes ticks and labels
        ax.set_xticks([])
        ax.set_yticks([])

        # Draw the grid lines based on the presence of letters
        for i in range(rows):
            for j in range(cols):
                cell_type = letters[i][j]
                if cell_type == '':
                    continue
                elif cell_type == '_':
                    rect = plt.Rectangle((j, rows - i - 1), 1, 1, facecolor='black', edgecolor='none')
                    ax.add_patch(rect)
                    rect = plt.Rectangle((j, rows - i - 1), 1, 1, facecolor='none', edgecolor='black', linewidth=1)
                    ax.add_patch(rect)
                else: 
                    # Draw a rectangle with a border around the cell
                    rect = plt.Rectangle((j, rows - i - 1), 1, 1, facecolor='none', edgecolor='black', linewidth=1)
                    ax.add_patch(rect)
                    # Place the letter in the center of the cell
                    letter = letters[i][j]
                    ax.text(j + 0.5, rows - i - 0.5, letter, fontsize=24, ha='center', va='center', color='black')

                    if letter.isupper():
                        ax.text(j + 0.05, rows - i - 0.9, str(word_index), fontsize=8, ha='left', va='top', color='black')
                        word_index += 1


        # Set equal aspect ratio to keep the cells square
        ax.set_aspect('equal')

        # Display the plot
        plt.xlim(0, cols)
        plt.ylim(0, rows)
        plt.gca().invert_yaxis()  # Invert the y-axis to have (0,0) at the top-left corner
        plt.show()
        # Set equal aspect ratio
        ax.set_aspect('equal')

        # Display the grid
        plt.show()


def create_crossword():

    # List of words to be added to the crossword
    max_overlaps = 0
    best_crossword = None
    for _ in range(200):
        words = ['Elephant_cage', 'Monkey', 'Money', 'Hat_of_pirate', 'Airplane', 'Hand', 'Fire_in_the_air', 'Queen', 'Rammstein', 'Foo_figters', 'Otis_redding', 'Smashing_pumpkins']
        random.shuffle(words)
        crossword = Crossword(words)
        overlaps = crossword.get_overlaps()
        if max_overlaps < overlaps:
            max_overlaps = overlaps
            best_crossword = crossword
    best_crossword.plot_crossword()
    print_dict_map(crossword.grid)


create_crossword()