# python modules:
import random
import json
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
        self.clear_widgets()
        languages = self.app.languages
        for word in self.app.words:
            box = BoxLayout(orientation="horizontal", size_hint_y=None, height=self.row_height)

            word1_label = Label(text=str(word[languages[0]]))
            word2_label = Label(text=str(word[languages[1]]))
            points_label = Label(text=str(word["points"]))

            box.add_widget(word1_label)
            box.add_widget(word2_label)
            box.add_widget(points_label)

            self.add_widget(box)


class Manager(ScreenManager):
    pass


class GameApp(App):
    points = kp.NumericProperty(settings.INIT_POINTS)
    languages = kp.ListProperty(["", ""])
    words = kp.ListProperty()
    number_of_words = kp.NumericProperty()
    current_word = kp.DictProperty()

    def build(self):
        self.manager = Manager()
        self.bind(words=self.calc_number_of_words)
        return self.manager

    def add_languages(self, lang1, lang2):
        self.languages = [lang1, lang2]

    def add_word(self, word1, word2):
        print("add_word(%s, %s)" % (word1, word2))
        new_word = {
            self.languages[0]: word1,
            self.languages[1]: word2
        }
        new_word["points"] = settings.INIT_WORD_POINTS
        self.words.append(new_word)

    def calc_number_of_words(self, *args):
        # print("number_of_words()", args)
        self.number_of_words = len(self.words)
        return self.number_of_words

    def pick_random_word(self, lang1="", lang2=""):
        print("pick_random_word(%s, %s)" % (lang1, lang2))
        if not lang1:
            lang1 = self.languages[0]
        if not lang2:
            lang2 = self.languages[1]
        if lang1 not in self.languages or lang2 not in self.languages or lang1 == lang2:
            raise Exception("please insert a valid languages not: %s and %s" % (lang1, lang2))
        return random.choice(self.words)

    def update_word_points(self, word1, word2):
        print("update_word_points(%s, %s)" % (word1, word2))
        for word in self.words:
            if word[self.languages[0]] == word1:
                if word[self.languages[1]] == word2 or word2 in word[self.languages[1]]:
                    word["points"] *= settings.POINTS["gain"]
                else:
                    word["points"] /= settings.POINTS["lose"]
                print("word: %s" % word)
                return word

    # GUI:
    def update_word_after_check(self, word1, word2):
        print("update_word_after_check(%s, %s)" % (word1, word2))
        self.current_word = self.update_word_points(word1, word2)
        print("self.current_word: %s" % self.current_word)
        game_menu = self.manager.game_menu
        game_menu.points_label.text = str(self.current_word["points"])
        self.save_game()

    def update_word(self):
        print("update_word()", self.current_word)
        self.current_word = self.pick_random_word()
        game_menu = self.manager.game_menu
        game_menu.points_label.text = str(self.current_word["points"])
        game_menu.word_label.text = self.current_word[self.languages[0]]
        game_menu.word_input.text = ""

    # load / save game:
    def load_game(self):
        try:
            with open(settings.SAVES_FILE) as f:
                data = json.load(f)
                self.points = data["points"]
                self.languages = data["languages"]
                self.words = data["words"]
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