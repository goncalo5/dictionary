# python modules:
import random
import json
import unicodedata
# kivy modules:
from kivy.app import App
from kivy import properties as kp
from kivy.core.window import Window
    # uix:
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.recycleview import RecycleView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
# mine:
import settings


# functions:
def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

# GUI:
class ListAllWords(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print(Window.height)
        self.row_height = min(Window.height / 10, 100)
        self.app = App.get_running_app()
        print(self.app.words)
        self.update_words()
        self.app.bind(words=self.update_words)

    def update_words(self, *args):
        print("update_words()", args)
        self.clear_widgets()
        languages = self.app.languages
        for word in self.app.words:
            box = BoxLayout(orientation="horizontal", size_hint_y=None, height=self.row_height)

            word1_label = Label(text=str(word[languages[0]]), size_hint_x=0.25)
            word2_label = Label(text=str(word[languages[1]]), size_hint_x=0.25)
            points_label = Label(text=str(round(word["points"], 2)), size_hint_x=0.25)
            delete_button = Button(text="Delete", size_hint_x=0.125)
            delete_button.word = word
            delete_button.bind(on_release=self.delete_word)
            edit_button = Button(text="Edit", size_hint_x=0.125)
            edit_button.word = word
            edit_button.bind(on_release=self.edit_word)

            box.add_widget(word1_label)
            box.add_widget(word2_label)
            box.add_widget(points_label)
            box.add_widget(edit_button)
            box.add_widget(delete_button)

            self.add_widget(box)

    def delete_word(self, *args):
        print("delete_word()", args, args[0].word)
        word = args[0].word
        self.app.delete_word(word)
        self.app.save_game()

    def edit_word(self, *args):
        print("edit_word()", args, args[0].word)
        word = args[0].word
        manager = self.app.meta_game.manager
        manager.current = "add_word_menu"
        manager.add_word_menu.language1_word.text = word[self.app.languages[0]]
        manager.add_word_menu.language2_word.text = word[self.app.languages[1]]
        self.app.words.remove(word)



class MetaGame(BoxLayout):
    pass


class GameApp(App):
    points = kp.NumericProperty(settings.POINTS["game"]["init"])
    languages = kp.ListProperty(["", ""])
    words = kp.ListProperty()
    number_of_words = kp.NumericProperty()
    current_word = kp.DictProperty()
    last_word = kp.DictProperty()

    def build(self):
        Window.size = (400, 600)
        self.meta_game = MetaGame()
        self.bind(words=self.calc_number_of_words)
        return self.meta_game

    def add_languages(self, lang1, lang2):
        self.languages = [lang1, lang2]

    def add_word(self, word1, word2):
        # print("add_word(%s, %s)" % (word1, word2))
        new_word = {
            self.languages[0]: word1,
            self.languages[1]: word2
        }
        new_word["points"] = settings.POINTS["word"]["init"]
        self.words.append(new_word)

    def delete_word(self, word_to_delete="", language=""):
        # print("delete_word()", word_to_delete, language)
        # word_to_delete could be a string or a dict/obj
        if not language:
            language = self.languages[0]
        if not isinstance(word_to_delete, str):
            word_to_delete = word_to_delete[language]
        for word in self.words:
            if word[language] == word_to_delete:
                self.words.remove(word)
                return

    def calc_number_of_words(self, *args):
        # print("number_of_words()", args)
        self.number_of_words = len(self.words)
        return self.number_of_words

    def pick_random_word(self, lang1="", lang2=""):
        print("\npick_random_word(%s, %s)" % (lang1, lang2))
        if not lang1:
            lang1 = self.languages[0]
        if not lang2:
            lang2 = self.languages[1]
        if lang1 not in self.languages or lang2 not in self.languages or lang1 == lang2:
            raise Exception("please insert a valid languages not: %s and %s" % (lang1, lang2))
        if len(self.words) == 1:
            return self.words[0]
        # calc n_of_words_to_choose_from
        # it depends of the points, more points -> more degree -> more difficult
        # if the degree is 0 all the words have the same prob to appear
        # if the degree is high, will always appear the same words (with less points)
        n_of_words_to_choose_from = self.number_of_words
        print("n_of_words_to_choose_from: %s" % n_of_words_to_choose_from)
        degree = int(self.points / 100)
        print("degree: %s" % degree)
        for _ in range(degree):
            n_of_words_to_choose_from = max(random.randrange(n_of_words_to_choose_from) + 1, 2)
            print("n_of_words_to_choose_from: %s" % n_of_words_to_choose_from)

        self.order_by("points")
        print("self.words:", self.words)
        possible_words_to_choose = self.words[0: n_of_words_to_choose_from]
        print("possible_words_to_choose", possible_words_to_choose)
        word_choosed = random.choice(possible_words_to_choose)
        print(word_choosed, self.last_word)
        print(word_choosed[self.languages[0]], self.last_word.get(self.languages[0], ""))
        if word_choosed[self.languages[0]] == self.last_word.get(self.languages[0], ""):
            print("word_choosed == self.last_word")
            possible_words_to_choose.remove(word_choosed)
            word_choosed = random.choice(possible_words_to_choose)

        return word_choosed

    def check_solution(self, word1, word2):
        print("self.languages", self.languages)
        for word in self.words:
            print("word", word)
            if word[self.languages[0]] == word1:
                correct_word = word[self.languages[1]]
                if isinstance(correct_word, str):
                    correct_word = [correct_word]
                # print("correct_word: %s" % correct_word)
                correct_word = [word.lower() for word in correct_word]
                if word2 and word2.lower() in correct_word:
                    # print("gain", correct_word == word2, word2 in correct_word)
                    return True, word
                else:
                    # print("lose", correct_word)
                    return False, word


    def update_word_points(self, word1, word2):
        # print("update_word_points(%s, %s)" % (word1, word2))
        increase_rate = settings.POINTS["word"]["increase_rate"]
        decreased_rate = settings.POINTS["word"]["decreased_rate"]
        is_correct, word = self.check_solution(word1, word2)
        if is_correct:
            word["points"] *= increase_rate
        else:
            word["points"] /= decreased_rate
        return word

    def update_points(self, word1, word2):
        print("update_points()", self.points)
        down4right_words = settings.POINTS["game"]["down4right_words"]
        up4wrong_words_a = settings.POINTS["game"]["up4wrong_words_a"]
        up4wrong_words_b = settings.POINTS["game"]["up4wrong_words_b"]
        is_correct, _ = self.check_solution(word1, word2)
        if is_correct:
            increment = up4wrong_words_a / ( self.points + up4wrong_words_b)
            self.points += increment
        else:
            self.points -= self.points / down4right_words

    def order_by(self, what, reverse=False):
        print("order_by(%s, %s)" % (what, reverse))
        # print(self.words)
        if what in ["points"]:
            self.words =\
                sorted(self.words, key=lambda x: float(x[what]), reverse=reverse)
        else:
            self.words =\
                sorted(self.words, key=lambda x: strip_accents(x[what]), reverse=reverse)
        # print(self.words)
        return self.words

    # GUI:
    def update_word_after_check(self, word1, word2):
        print("update_word_after_check(%s, %s)" % (word1, word2))
        # print("self.current_word: %s" % self.current_word)
        self.current_word = self.update_word_points(word1, word2)
        self.update_points(word1, word2)
        # print("self.current_word: %s" % self.current_word)
        game_menu = self.meta_game.manager.game_menu
        game_menu.points_label.text = "Word Points: %s" % round(self.current_word["points"], 2)
        game_menu.word_input.text = str(self.current_word[self.languages[1]])
        self.save_game()

    def update_word(self):
        print("update_word()", self.current_word)
        self.last_word = self.current_word.copy()
        print("self.last_word:", self.last_word)
        self.current_word = self.pick_random_word()
        print("self.current_word:", self.current_word)
        game_menu = self.meta_game.manager.game_menu
        game_menu.points_label.text = "Word Points: %s" % round(self.current_word["points"], 2)
        game_menu.word_label.text = self.current_word[self.languages[0]]
        game_menu.word_input.text = ""

    def quit(self):
        print("quit()")
        print(self.meta_game.manager.current)
        print(self.meta_game.manager.current_screen.previous_screen)
        previous_screen = self.meta_game.manager.current_screen.previous_screen
        if previous_screen:
            self.meta_game.manager.current = previous_screen
        else:
            exit()
            


    # load / save game:
    def load_game(self):
        try:
            with open(settings.SAVES_FILE) as f:
                data = json.load(f)
                self.points = data["points"]
                self.languages = data["languages"]
                self.words = data["words"]
                self.calc_number_of_words()
        except FileNotFoundError:
            pass

    def save_game(self):
        with open(settings.SAVES_FILE, "w") as f:
            data = {
                "points": self.points,
                "languages": self.languages,
                "words": self.words
            }
            json.dump(data, f, indent=4) 


if __name__ == "__main__":
    game_app = GameApp()
    game_app.load_game()
    game_app.run()