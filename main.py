import wordle
import pygame
import sys

# wordle.filter_words_func() # only use if 5 letter word list does not already exist and contain correct words

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
            "bold": pygame.font.SysFont("wordle/assets/ClearSans-Bold.ttf", 100),
            "thin": pygame.font.SysFont("wordle/assets/ClearSans-Thin.ttf", 100),
            "light": pygame.font.SysFont("wordle/assets/ClearSans-Light.ttf", 100),
            "medium": pygame.font.SysFont("wordle/assets/ClearSans-Medium.ttf", 100),
            "regular": pygame.font.SysFont("wordle/assets/ClearSans-Bold.ttf", 100),
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
        self.history = []
        self.current_words = [
            [" ", " ", " ", " ", " ", False],
            [" ", " ", " ", " ", " ", False],
            [" ", " ", " ", " ", " ", False],
            [" ", " ", " ", " ", " ", False],
            [" ", " ", " ", " ", " ", False],
            [" ", " ", " ", " ", " ", False],
        ]
        
        self.running = True
        
        self.add_words()
        
        self.execute()
        
    def add_words(self) -> None:
        """ Add words to an array of words, stores in instance of class """
        file = open("wordle/words/five_letter_words.txt", "r")
        self.all_words = file.readlines()
    
    def logic(self) -> None:
        """ Controls the game logic """
        
    
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
        
        for i in range(5):
            print(i)
        
        self._display_surface.fill(self.colours["content_background"])
        
        # self._display_surface.blit(self.test_text, self.text_text_rect)
        
        pygame.display.update()
        
        
    def on_event(self, event) -> None:
        """ Handles events """
        if event.type == pygame.QUIT:
            self.quit()
    def quit(self) -> None:
        """ Exits pygame, then the program """
        pygame.quit()
        sys.exit(0)
    
        

if __name__ == "__main__":
    game = Game()