import wordle

# wordle.filter_words_func() -> only use if 5 letter word list does not already exist and contain correct words

class Game():
    def __init__(self) -> None:
        self.words = []
        
        self.add_words()
        
    def add_words(self) -> None:
        file = open("wordle/words/five_letter_words.txt", "r")
        self.words = file.readlines()
    
    def take_input(self) -> str:
        user_input = input("")
        return user_input
    
    def logic(self) -> None:
        
    
    
    


if __name__ == "__main__":
    game = Game()