import pygame
import sys
import itertools

from string import ascii_uppercase, ascii_letters

# wordle.filter_words_func() # only use if 5 letter word list does not already exist and contain correct words

# What the cells array looks like: 
# [
#     [{"id": "00", "content": " ", "state": 0, "background_colour": " ", "rect": }, {}, {}, {}, {}, False],
#     [{}, {}, {}, {}, {}, False],
#     [{}, {}, {}, {}, {}, False],
#     [{}, {}, {}, {}, {}, False],
#     [{}, {}, {}, {}, {}, False],
#     [{}, {}, {}, {}, {}, False],
# ]

class Game():
    """ Class to control the game """
    def __init__(self) -> None:
        """ Initalises Game class, initialises pygame, creates Game variables """
        pygame.init()
        
        self.window_width = 800
        self.window_height = 800
        self.caption = "Wordle by Sam Chandler"
        self._display_surface = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(self.caption)
        self.fps_clock = pygame.time.Clock()
        self.FPS = 60
        self.fonts = {
            "bold": pygame.font.Font("python-wordle\\game\\assets\\ClearSans-Bold.ttf", 75),
            "thin": pygame.font.Font("python-wordle\\game\\assets\\ClearSans-Thin.ttf", 75),
            "light": pygame.font.Font("python-wordle\\game\\assets\\ClearSans-Light.ttf", 75),
            "medium": pygame.font.Font("python-wordle\\game\\assets\\ClearSans-Medium.ttf", 75),
            "regular": pygame.font.Font("python-wordle\\game\\assets\\ClearSans-Regular.ttf", 75),
        } # all fonts
        
        self.colours = {
            "text": "#ffffff",
            "content_background": "#121213",

            "letter_correct": "#538d4e",
            "letter_present": "#b59f3b",
            "letter_absent": "#3a3a3c",
            "letter_border": "#3a3a3c",

            "keyboard_background": "#818384",
            "keyboard_correct": "#538d4e",
            "keyboard_present": "#b59f3b",
            "keyboard_absent": "#3a3a3c",
        } # all colours
        
        # self.test_text = self.fonts["bold"].render("This is a test", True, self.colours["text"])
        # self.text_text_rect = self.test_text.get_rect()
        # self.text_text_rect.center = (self.window_width / 2, self.window_height / 2)

        self.all_words = []
        self.cell_size = 75
        self.cell_gap = 5
        self.top_gap = self.cell_size + (self.cell_gap * 5)
        self.left_gap = ((self.cell_size * 5) + (self.cell_gap * 4)) / 2
        
        self.title_text = self.fonts["bold"].render("Wordle in Python", True, self.colours["text"])
        self.title_text_rect = self.title_text.get_rect()
        self.title_text_rect.center = (self.window_width // 2, 40)
        
        self.keyboard_letters = {}
        
        self.running = True
        
        self.add_words()
        self.create_keyboard_letters()
        self.create_cells()
        self.initialise_letters()
        
        self.execute()
        
    def add_words(self) -> None:
        """ Add words to an array of words, stores in instance of class """        
        file = open("python-wordle\\game\\assets\\five_letter_words.txt", "r")
        self.all_words = file.readlines()
    
    def logic(self) -> None:
        """ Controls the game logic """
        
    def initialise_letters(self) -> None:
        letters = {}
        for letter in ascii_uppercase:
            letter_text = self.fonts["bold"].render(letter, True, self.colours["text"])
            letter_text_rect = letter_text.get_rect()
            letters[letter] = [
                self.fonts["bold"].render(letter, True, self.colours["text"]), 
                letter_text_rect
                ]
        self.letters = letters
    
    def create_keyboard_letters(self) -> None:
        """ Adds all letters to a data dictionary 
        Letter states:
        0: unused
        1: absent
        2: present
        3: correct
        """
        for letter in ascii_uppercase:
            self.keyboard_letters[letter] = 0
        
    def create_cells(self) -> None:
        """ Creates data dictionary of all cells in the game """    

        cells = []
        rows = 6
        columns = 5
        
        for i in range(rows):
            column = []
            for j in range(columns + 1):
                if j == columns:
                    column.append(False)
                else:
                    column.append({
                        "id": f"{i}{j}", 
                        "content": " ", 
                        "state": " ", 
                        "background_colour": None, 
                        "rect": pygame.Rect(
                                self.left_gap + (j * self.cell_size) + (j * self.cell_gap),
                                self.top_gap + (i * self.cell_size) + (i * self.cell_gap) + 20,
                                self.cell_size,
                                self.cell_size
                                )
                    })
            cells.append(column)
            
        self.cells = cells
           
    def execute(self) -> None:
        """ Controls while loop of game """
        while self.running:
            for event in pygame.event.get():
                self.on_event(event)
                    
            self.logic()
            self.render()
            self.fps_clock.tick(self.FPS)
                       
    def render(self) -> None:
        """ Renders elements onto screen """
        
        self._display_surface.fill(self.colours["content_background"])
        self._display_surface.blit(self.title_text, self.title_text_rect)
        
        pygame.draw.line(self._display_surface, self.colours["text"], (0, self.cell_size + 15), (self.window_width, self.cell_size + 15), 1)
        
        for row in self.cells:
            for cell in itertools.islice(row, 5):
                pygame.draw.rect(self._display_surface, self.colours["letter_absent"], cell["rect"], 2)
                if cell["content"] != " ":
                    print(cell["content"], cell["id"])
            
        # self._display_surface.blit(self.test_text, self.text_text_rect)
        
        pygame.display.update()  
        
    def on_event(self, event) -> None:
        """ Handles events """
        if event.type == pygame.QUIT:
            self.quit()
        if event.type == pygame.KEYDOWN:
            # Enter : 13
            # Backspace : 8

            try:
                character = chr(event.key).upper()
                if character in ascii_uppercase:
                    cell_id_to_insert_letter = self.search_for_first_empty_cell()
                    for row in self.cells:
                        for cell in itertools.islice(row, 5):
                            if cell["id"] == cell_id_to_insert_letter:
                                cell["content"] = character

            except ValueError as error:
                pass

    def search_for_first_empty_cell(self) -> str:
        for row in self.cells:
            for cell in itertools.islice(row, 5):
                if cell["content"] == " ":
                    return cell["id"]
        return ""
    
    def quit(self) -> None:
        """ Exits pygame, then the program """
        pygame.quit()
        sys.exit(0)

    def filter_words_func(self):
        all_words_file = open("python-wordle\\game\\assets\\words.txt", "r")
        five_letter_words_file = open("python-wordle\\game\\assets\\five_letter_words.txt", "w")
        all_words = all_words_file.readlines()
        for word in all_words:
            valid = True
            index = 0
            for letter in word:
                if not str(letter) in ascii_letters and index < 5:
                    valid = False
                index += 1
            if len(word) == 6 and valid:
                five_letter_words_file.write(word.upper())
        all_words_file.close()
        five_letter_words_file.close()

if __name__ == "__main__":
    game = Game()