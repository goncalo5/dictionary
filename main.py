# kivy modules:
from kivy.app import App
from kivy import properties as kp
from kivy.core.window import Window
    # uix:
from kivy.uix.screenmanager import ScreenManager, Screen
# mine:
import settings

# game = {
#     "points": settings.INIT_POINTS
# }


class Manager(ScreenManager):
    pass


class GameApp(App):
    points = kp.NumericProperty(settings.INIT_POINTS)
    languages = kp.ListProperty(["", ""])
    words = kp.ListProperty()

    def build(self):
        self.manager = Manager()
        return self.manager

    def add_languages(self, lang1, lang2):
        self.languages = [lang1, lang2]

    def add_word(self, word1, word2):
        new_word = {
            self.languages[0]: word1,
            self.languages[1]: word2
        }
        new_word["points"] = settings.INIT_WORD_POINTS
        self.words.append(new_word)


if __name__ == "__main__":
    GameApp().run()