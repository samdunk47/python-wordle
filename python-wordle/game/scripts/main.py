import pygame
import sys
from itertools import islice
from random import randint
from pprint import pprint

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
            "small": pygame.font.Font("python-wordle\\game\\assets\\ClearSans-Bold.ttf", 20),
            "large": pygame.font.Font("python-wordle\\game\\assets\\ClearSans-Bold.ttf", 125),
        } # all fonts
        
        self.colours = {
            "text": "#ffffff",
            "content_background": "#121213",

            "letter_unused": "#121213",
            "letter_absent": "#3a3a3c",
            "letter_present": "#b59f3b",
            "letter_correct": "#538d4e",
            
            "letter_border": "#3a3a3c",

            "keyboard_unused": "#818384",
            "keyboard_correct": "#538d4e",
            "keyboard_present": "#b59f3b",
            "keyboard_absent": "#3a3a3c",
        } # all colours
        
        # self.test_text = self.fonts["bold"].render("This is a test", True, self.colours["text"])
        # self.text_text_rect = self.test_text.get_rect()
        # self.text_text_rect.center = (self.window_width / 2, self.window_height / 2)

        self.all_words = []
        self.all_answer_words = []
        self.cell_size = 75
        self.cell_gap = 5
        self.top_gap = self.cell_size + (self.cell_gap * 5)
        self.left_gap = ((self.cell_size * 5) + (self.cell_gap * 4)) / 2
        
        self.current_row = 0
        self.chosen_word = ""
        self.won = False
        self.lost = False
        
        self.title_text = self.fonts["bold"].render("Wordle in Python", True, self.colours["text"])
        self.title_text_rect = self.title_text.get_rect()
        self.title_text_rect.center = (self.window_width // 2, 40)
        
        self.won_text = self.fonts["large"].render("You won!", True, self.colours["text"])
        self.won_text_rect = self.won_text.get_rect()
        self.won_text_rect.center = (self.window_width // 2, 650)
        
        self.lost_text = self.fonts["large"].render("You lost!", True, self.colours["text"])
        self.lost_text_rect = self.lost_text.get_rect()
        self.lost_text_rect.center = (self.window_width // 2, 650)
        
        self.play_again_text = self.fonts["bold"].render("Play again", True, self.colours["text"])
        self.play_again_text_rect = self.play_again_text.get_rect()
        
        self.keyboard_letters = []
            
        self.running = True
        
        self.add_words()
        self.create_keyboard_letters()
        self.create_cells()
        self.initialise_letters()
        
        self.logic()
        self.execute()

    def add_words(self) -> None:
        """ Add words to an array of words, stores in instance of class """        
        words_file = open("python-wordle\\game\\assets\\words.txt", "r")
        all_words_with_newlines = words_file.readlines()
        all_words = []
        for word in all_words_with_newlines:
            all_words.append(word.replace("\n", ""))
        self.all_words = all_words

        answer_words_file = open("python-wordle\\game\\assets\\answer_words.txt", "r")
        all_answer_words_with_newlines = answer_words_file.readlines()
        all_answer_words = []
        for word in all_answer_words_with_newlines:
            all_answer_words.append(word.replace("\n", ""))
        self.all_answer_words = all_answer_words
        
    def initialise_letters(self) -> None:
        letters = {}
        for letter in ascii_uppercase:
            letters[letter] = 0
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
            self.keyboard_letters.append(
                {"letter": letter, "state": 0, "background_colour": self.colours["keyboard_unused"], "rect": None}
            )
        
        width = 40
        height = 50
        width_gap = 10
        height_gap = 10
        
        for key, letter in enumerate(islice(self.keyboard_letters, 0, 9)):
            x_cor = 176.25 + (key * width) + (key * width_gap)
            y_cor = 620
            self.keyboard_letters[key]["rect"] = pygame.Rect(x_cor, y_cor, width, height)
            
        for key, letter in enumerate(islice(self.keyboard_letters, 9, 18)):
            x_cor = 176.25 + (key * width) + (key * width_gap)
            y_cor = 670 + height_gap
            key += 9
            self.keyboard_letters[key]["rect"] = pygame.Rect(x_cor, y_cor, width, height)
            
        for key, letter in enumerate(islice(self.keyboard_letters, 18, 26)):
            x_cor = 201.25 + (key * width) + (key * width_gap)
            y_cor = 720 + (height_gap * 2)
            key += 18
            self.keyboard_letters[key]["rect"] = pygame.Rect(x_cor, y_cor, width, height)

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
                        "state": 0, 
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
                
            self.render()
            self.check_win()
            self.fps_clock.tick(self.FPS)
                       
    def render(self) -> None:
        """ Renders elements onto screen """
        
        self._display_surface.fill(self.colours["content_background"])
        self._display_surface.blit(self.title_text, self.title_text_rect)
        
        pygame.draw.line(self._display_surface, self.colours["text"], (0, self.cell_size + 15), (self.window_width, self.cell_size + 15), 1)
    
        
        for row in self.cells:
            for cell in islice(row, 5):
                    pygame.draw.rect(self._display_surface, cell["background_colour"], cell["rect"])
                    pygame.draw.rect(self._display_surface, self.colours["letter_absent"], cell["rect"], 2)
                    if cell["content"] != " ":
                        letter = cell["content"]
                        letter_text = self.fonts["bold"].render(letter, True, self.colours["text"])
                        letter_text_rect = letter_text.get_rect()
                        letter_text_rect.center = ((cell["rect"][0] + (self.cell_size / 2)),
                                                (cell["rect"][1] + (self.cell_size / 2)) - 5)
                        self._display_surface.blit(letter_text, letter_text_rect)

        if not self.won and not self.lost:
            for letter in self.keyboard_letters:
                pygame.draw.rect(self._display_surface, letter["background_colour"], letter["rect"], border_radius=2)
                letter_text = self.fonts["small"].render(letter["letter"], True, self.colours["text"])
                letter_text_rect = letter_text.get_rect()
                letter_text_rect.center = ((letter["rect"][0] + 20),
                                            (letter["rect"][1] + 25) - 2.5)
                self._display_surface.blit(letter_text, letter_text_rect)
        
        if self.won:
            # pygame.draw.rect(self._display_surface, "#999999", pygame.Rect(self.won_text_rect[0] - 25, self.won_text_rect[1] + 25, self.won_text_rect[2] + 50, self.won_text_rect[3] - 25), 10)
            self._display_surface.blit(self.won_text, self.won_text_rect)
            
            
        if self.lost:
            self._display_surface.blit(self.lost_text, self.lost_text_rect)
                 
        # self._display_surface.blit(self.test_text, self.text_text_rect)
        
        pygame.display.update()  
        
    def on_event(self, event) -> None:
        """ Handles events """
        if event.type == pygame.QUIT:
            self.quit()
        elif event.type == pygame.KEYDOWN and not self.won:
            # Enter : 13
            # Backspace : 8

            try:
                character = chr(event.key).upper()
                if character in ascii_uppercase:
                    self.input_character(character)
            except ValueError:
                pass
            
            if event.key == 13:
                self.on_enter_press()
            elif event.key == 8:
                self.on_backspace_press()
                
        self.update_cell_colours()
        self.logic()

    
    def logic(self) -> None:
        """ Controls the game logic """
        if self.chosen_word == "":
            number_of_words = len(self.all_answer_words)
            random_number = randint(0, number_of_words)
            self.chosen_word = self.all_answer_words[random_number]
            print(f"chosen word: '{self.chosen_word}'")

        for row in islice(self.cells, self.current_row, len(self.cells)):
            if row[5] == True:
                self.current_row += 1
        
    def check_valid_word(self, word) -> bool:
        if word in self.all_words:
            return True
        return False    
    
    def find_row_word(self, row_to_check) -> str:
        row_word = ""
        for row in self.cells:
            if self.cells.index(row) == row_to_check:
                for cell in islice(row, 5):
                    row_word += cell["content"]

        return row_word
    
    def input_character(self, character) -> None:
        cell_id_to_insert_letter = self.search_for_first_empty_cell()
        for row in self.cells:
            for cell in islice(row, 5):
                if cell["id"] == cell_id_to_insert_letter and int(cell["id"][0]) == self.current_row:
                    cell["content"] = character
    
    def on_enter_press(self) -> None:
        try:
            if self.cells[self.current_row][4]["content"] != " ":
                current_row_word = self.find_row_word(self.current_row).lower()
                if current_row_word.upper() in self.all_words:
                    self.cells[self.current_row][5] = True
                    
                    for cell in islice(self.cells[self.current_row], 5):
                        if cell["content"] != " ":
                            letter = cell["content"].lower()
                            if letter in self.chosen_word:
                                if self.chosen_word.index(letter) == current_row_word.index(letter):
                                    self.letters[letter.upper()] = 3
                                else:
                                    self.letters[letter.upper()] = 2
                            else:
                                self.letters[letter.upper()] = 1
                                
                self.update_state_values()
                
                    # for keyboard_letter in self.keyboard_letters:
                    #     letter = keyboard_letter["letter"].lower()
                    #     print(letter)
                    #     if letter in self.chosen_word:
                    #         if self.chosen_word.index(letter) == current_row_word.index(letter):
                    #             keyboard_letter["state"] = 3
                    #         else:
                    #             keyboard_letter["state"] = 2
                    #     else:
                    #         keyboard_letter["state"] = 1
                     
        except IndexError:
            pass   
    
    def update_state_values(self) -> None:
        for row in self.cells:
            for cell in islice(row, 5):
                if cell["content"] != " ":
                    cell["state"] = self.letters[cell["content"]]
        
        for letter in self.keyboard_letters:
            letter["state"] = self.letters[letter["letter"]]
    
    def check_win(self) -> None:
        if self.find_row_word(self.current_row - 1).upper() == self.chosen_word.upper():
            if self.cells[self.current_row - 1][5] == True:
                self.won = True
        if self.cells[5][5] == True and self.won == False:
            self.lost = True

    def on_backspace_press(self) -> None:
        first_empty_cell = self.search_for_first_empty_cell()
        try:
            recent_cell = str(first_empty_cell[0] + str((int(first_empty_cell[1]) - 1 )))
        except IndexError:
            recent_cell = "54"
        if len(recent_cell) > 2:
            new_cell = str(int(recent_cell[0]) - 1) + "4"
            recent_cell = new_cell
            
        for row in self.cells:
            for cell in islice(row, 5):
                if cell["id"] == recent_cell and recent_cell[0] == str(self.current_row):
                    cell["content"] = " "
        
    def search_for_first_empty_cell(self) -> str:
        for row in self.cells:
            for cell in islice(row, 5):
                if cell["content"] == " ":
                    return cell["id"]
        else:
            return ""

    def update_cell_colours(self) -> None:
        for row in self.cells:
            for cell in islice(row, 5):
                match cell["state"]:
                    case 0:
                        cell["background_colour"] = self.colours["letter_unused"]
                    case 1:
                        cell["background_colour"] = self.colours["letter_absent"]
                    case 2:
                        cell["background_colour"] = self.colours["letter_present"]
                    case 3:
                        cell["background_colour"] = self.colours["letter_correct"]
                        
        for letter in self.keyboard_letters:
            match letter["state"]:
                case 0:
                    letter["background_colour"] = self.colours["keyboard_unused"]
                case 1:
                    letter["background_colour"] = self.colours["keyboard_absent"]
                case 2:
                    letter["background_colour"] = self.colours["keyboard_present"]
                case 3:
                    letter["background_colour"] = self.colours["keyboard_correct"]
    
    
    def quit(self) -> None:
        """ Exits pygame, then the program """
        pygame.quit()
        sys.exit(0)

    # def filter_words_func(self):
    #     all_words_file = open("python-wordle\\game\\assets\\words.txt", "r")
    #     five_letter_words_file = open("python-wordle\\game\\assets\\five_letter_words.txt", "w")
    #     all_words = all_words_file.readlines()
    #     for word in all_words:
    #         valid = True
    #         index = 0
    #         for letter in word:
    #             if not str(letter) in ascii_letters and index < 5:
    #                 valid = False
    #             index += 1
    #         if len(word) == 6 and valid:
    #             five_letter_words_file.write(word.upper())
    #     all_words_file.close()
    #     five_letter_words_file.close()

if __name__ == "__main__":
    game = Game()