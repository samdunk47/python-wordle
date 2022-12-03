import wordle
import pygame
import sys

# wordle.filter_words_func() -> only use if 5 letter word list does not already exist and contain correct words

class Game():
    def __init__(self) -> None:
        """ Initalises Game class, initialises pygame, creates Game variables """
        pygame.init()
        
        self.words = []
        self.history = []
        
        self.window_width = 800
        self.window_height = 800
        self.caption = "Wordle by Sam Chandler"
        self._display_surface = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(self.caption)
        
        self.colours = {
            "background": 
        }
        self.running = True
        
        self.add_words()
        
    def add_words(self) -> None:
        """ Add words to an array of words, stores in instance of class """
        file = open("wordle/words/five_letter_words.txt", "r")
        self.words = file.readlines()
    
    def execute(self) -> None:
        """ Controls while loop of game """
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                    
            self.render()
            
    def render(self) -> None:
        """ Renders elements onto screen """
        pygame.display.update()
        
        
    def on_event(self, event) -> None:
        """ Handles events """
        
    def quit(self) -> None:
        """ Exits pygame, then the program """
        pygame.quit()
        sys.exit(0)
    
        

if __name__ == "__main__":
    game = Game()