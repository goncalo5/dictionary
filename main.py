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


if __name__ == "__main__":
    GameApp().run()