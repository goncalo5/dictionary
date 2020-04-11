INIT_POINTS = 500
INIT_WORD_POINTS = 1

POINTS = {
    "game": {

        "init": 500,
        # will be divided by
        "down4right_words": 50,
        # increment = self.up4wrong_words_a / ( self.word_points + self.up4wrong_words_b)
        "up4wrong_words_a": 10000,
        "up4wrong_words_b": 20
    },
    "word": {
        "init": 1,
        "increase_rate": 1.5,
        "decreased_rate": 5.0
    }
}
SAVES_FILE = "dictionary.json"