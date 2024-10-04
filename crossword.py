from typing import List
from ut import Vec2D, print_dict_map
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt

class Crossword:
    def __init__(self, words: List[str]):
        self.grid = {}
        # Generate the grid
        for word in words: 
            self.place_word(word=word)

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
        for word_i, new_char in enumerate(word):
            for pos, char in self.grid.items():
                if new_char == char:
                    if self.try_place_word(word=word, pos=pos, word_i=word_i):
                        return

        if self.grid == {}:
            self.try_place_word(word=word, pos=Vec2D(0, 0), word_i=0)

    def draw_crossword(self):
        # Find the max x and y values to size the grid
        max_x = max(pos.x for pos in self.grid.keys())
        min_x = min(pos.x for pos in self.grid.keys())
        max_y = max(pos.y for pos in self.grid.keys())
        min_y = min(pos.y for pos in self.grid.keys())
        
        size_x = max_x - min_x
        size_y = max_y - min_y

        # Create the figure and axis
        fig, ax = plt.subplots(figsize=(size_y, size_x))
        
        # Create grid with empty spaces
        grid = np.full((size_x, size_y), '', dtype=str)
        
        # Populate grid with the crossword letters
        for pos, letter in self.grid.items():
            grid[pos.x][pos.y] = letter
        
        # Plot the crossword
        ax.imshow(np.ones_like(grid, dtype=int), cmap='Greys', extent=(min_y, max_y, min_x, max_x))
        
        # Add letters to each grid cell
        for pos, letter in self.grid.items():
            ax.text(pos.y + 0.5, max_x - pos.x - 0.5, letter, va='center', ha='center', fontsize=16, family='monospace')
        
        # Hide axis ticks
        ax.set_xticks(np.arange(max_y + 1))
        ax.set_yticks(np.arange(max_x + 1))
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.grid(True, which='both', color='black', linewidth=2)
        
        plt.show()


# List of words to be added to the crossword
words = ['elephant', 'monkey', 'money', 'hat', 'airplane']

crossword = Crossword(words)
crossword.draw_crossword()
print_dict_map(crossword.grid)
