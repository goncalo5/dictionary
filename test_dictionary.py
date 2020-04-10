#!/usr/bin/python
import unittest
import dictionary
import actions
import main
from settings import *


class TestDictionary(unittest.TestCase):

    def setUp(self):
        self.words = {
            "words": []
        }
        self.house_word = {
            "en": "house",
            "pt": "casa",
            "points": 1
        }
        self.tree_word = {
            "en": "tree",
            "pt": "árvore",
            "points": 1
        }

    def test_add_languages(self):
        game_app = main.GameApp()
        game_app.add_languages("en", "pt")
        self.assertEqual(game_app.languages, ["en", "pt"])

    def test_add_word(self):
        game_app = main.GameApp()
        game_app.add_languages("en", "pt")

        game_app.add_word("house", "casa")
        sol = {"en": "house", "pt": "casa", "points": INIT_WORD_POINTS}
        self.assertIn(sol, game_app.words)

        game_app.add_word("house", ["casa", "vivenda"])
        sol = {"en": "house", "pt": ["casa", "vivenda"], "points": INIT_WORD_POINTS}
        self.assertIn(sol, game_app.words)

    def test_delete_word(self):
        print("\ntest_delete_word()")
        game_app = main.GameApp()
        game_app.add_languages("en", "pt")
        game_app.add_word("house", "casa")
        game_app.delete_word("house", "en")
        self.assertEqual([], game_app.words)
        game_app.add_word("house", "casa")
        game_app.add_word("tree", "árvore")
        game_app.delete_word("tree", "en")
        self.assertEqual([self.house_word], game_app.words)
        game_app.delete_word(self.house_word)
        self.assertEqual([], game_app.words)
        game_app.add_word("house", "casa")
        game_app.delete_word("house")
        self.assertEqual([], game_app.words)
        game_app.add_word("house", "casa")
        game_app.delete_word("tree")
        self.assertEqual([self.house_word], game_app.words)


    def test_number_of_words(self):
        print()
        game_app = main.GameApp()
        game_app.add_languages("en", "pt")
        self.assertEqual(game_app.calc_number_of_words(), 0)
        game_app.add_word("house", "casa")
        self.assertEqual(game_app.calc_number_of_words(), 1)

    def test_pick_random_word(self):
        print("\ntest_pick_random_word()")
        game_app = main.GameApp()
        game_app.add_languages("en", "pt")
        game_app.add_word("house", "casa")
        self.assertEqual(game_app.pick_random_word("en", "pt"), {"en": "house", "pt": "casa", "points": 1})
        self.assertEqual(game_app.pick_random_word("pt", "en"), {"pt": "casa", "en": "house", "points": 1})
        with self.assertRaises(Exception):
            game_app.pick_random_word("pt", "en1")
        self.assertEqual(game_app.pick_random_word(), {"en": "house", "pt": "casa", "points": 1})

    def test_update_word_points(self):
        print("\ntest_update_word_points()")
        game_app = main.GameApp()
        game_app.add_languages("en", "pt")
        game_app.add_word("tree", "árvore")
        sol = {"en": "tree", "pt": "árvore", "points": INIT_WORD_POINTS * POINTS["gain"]}
        self.assertEqual(game_app.update_word_points("tree", "árvore"), sol)
        game_app.add_word("house", ["casa", "vivenda"])
        sol = {"en": "house", "pt": ["casa", "vivenda"], "points": INIT_WORD_POINTS * POINTS["gain"]}
        self.assertEqual(game_app.update_word_points("house", "casa"), sol)
        sol["points"] /= POINTS["lose"]
        self.assertEqual(game_app.update_word_points("house", "casaa"), sol)
        sol["points"] /= POINTS["lose"]
        self.assertEqual(game_app.update_word_points("house", ""), sol)
        game_app.add_word("brew", "preparar")
        sol = {"en": "brew", "pt": "preparar", "points": INIT_WORD_POINTS / POINTS["lose"]}
        self.assertEqual(game_app.update_word_points("brew", ""), sol)

    def test_order_by(self):
        print("\ntest_order_by()")
        game_app = main.GameApp()
        game_app.add_languages("en", "pt")
        game_app.add_word("tree", "árvore")
        game_app.add_word("house", "casa")
        game_app.update_word_points("house", "casa")
        self.tree_word["points"] = INIT_WORD_POINTS
        self.house_word["points"] = INIT_WORD_POINTS * POINTS["gain"]
        self.assertEqual(game_app.order_by("points"), [self.tree_word, self.house_word])
        self.assertEqual(game_app.order_by("points", True), [self.house_word, self.tree_word])
        self.assertEqual(game_app.order_by("en"), [self.house_word, self.tree_word])
        self.assertEqual(game_app.order_by("pt"), [self.tree_word, self.house_word])


# class TestWizard(unittest.TestCase):

    # def setUp(self):
    #     self.run = dictionary.Run()
    #     self.dict_of_all_words = {
    #         1.: ["hello", "ola"], 25.69675451079: ["hero", "her\u00f3i"],
    #         2.: ["cart", "carrinho/carro\u00e7a"], 30.26948287757: ["ship", "barco/navio"],
    #         }

    # def test_check_if_the_points_exist(self):
    #     # print a.dict_of_all_words
    #     result = self.run.check_if_the_points_exist(2., self.dict_of_all_words)
    #     self.assertEqual(result, True)
    #     result = self.run.check_if_the_points_exist(2.1, self.dict_of_all_words)
    #     self.assertEqual(result, False)
    #     result = self.run.check_if_the_points_exist(25.69675451079, self.dict_of_all_words)
    #     self.assertEqual(result, True)
    #     result = self.run.check_if_the_points_exist(25.696754510795, self.dict_of_all_words)
    #     self.assertEqual(result, False)
    #     result = self.run.check_if_the_points_exist(25.6967545107, self.dict_of_all_words)
    #     self.assertEqual(result, False)

    # def test_create_valide_points(self):
    #     result = self.run.create_valide_points(10., self.dict_of_all_words)
    #     self.assertEqual(result, 10.)
    #     result = self.run.create_valide_points(2., self.dict_of_all_words)
    #     self.assertGreater(result, 2.)
    #     result = self.run.create_valide_points(30.26948287757, self.dict_of_all_words)
    #     self.assertGreater(result, 30.26948287757)

    #     result = self.run.create_valide_points(30.26948287757, self.dict_of_all_words)
    #     result = round(result, 2)
    #     self.assertEqual(result, 30.27)

    # def test_check_if_the_word_exist(self):
    #     result = self.run.check_if_the_word_exist("hero", self.dict_of_all_words)
    #     self.assertEqual(result, 25.69675451079)
    #     result = self.run.check_if_the_word_exist("cart", self.dict_of_all_words)
    #     self.assertEqual(result, 2.)
    #     result = self.run.check_if_the_word_exist("unknown", self.dict_of_all_words)
    #     self.assertEqual(result, None)

    # def test_add_new_word(self):
    #     new_dict = self.dict_of_all_words.copy()
    #     result = self.run.add_new_word(
    #         new_word=["hello", "ola"], new_word_points=1., dictionary=new_dict)
    #     self.assertEqual(result, None)

    #     new_dict = self.dict_of_all_words.copy()
    #     self.run.add_new_word(
    #         new_word=["unknown", "nao sei"], new_word_points=1., dictionary=new_dict)
    #     new_dict.update({1.: ["unknown", "nao sei"]})
    #     self.assertEqual(new_dict, new_dict)

    #     new_dict = self.dict_of_all_words.copy()
    #     self.run.add_new_word(
    #         new_word=["unknown", "nao sei"], new_word_points=25.69675451079,
    #         dictionary=new_dict)
    #     self.assertEqual(len(new_dict), len(self.dict_of_all_words) + 1)

    # def test_delete_word(self):
    #     new_dict = self.dict_of_all_words.copy()
    #     self.run.delete_word(original_word="hello", dictionary=new_dict)
    #     self.assertEqual(len(new_dict), len(self.dict_of_all_words) - 1)

    #     new_dict = self.dict_of_all_words.copy()
    #     self.run.delete_word(original_word="unknown", dictionary=new_dict)
    #     self.assertEqual(len(new_dict), len(self.dict_of_all_words))

    # def test_calc_word_points(self):
    #     result = self.run.calc_word_points(
    #         dictionary=self.dict_of_all_words, words_score=200, last_word_points=2.)
    #     self.assertNotEqual(result, 2.)
    #     self.assertIn(result, self.dict_of_all_words)
    #     result = self.run.calc_word_points(
    #         dictionary=self.dict_of_all_words, words_score=800, last_word_points=1.)
    #     self.assertNotEqual(result, 1.)
    #     self.assertIn(result, self.dict_of_all_words)
    #     result = self.run.calc_word_points(
    #         dictionary=self.dict_of_all_words, words_score=50, last_word_points=30.26948287757)
    #     self.assertNotEqual(result, 30.26948287757)
    #     self.assertIn(result, self.dict_of_all_words)

    # def test_choose_a_word(self):
    #     result = self.run.choose_a_word(
    #         dictionary=self.dict_of_all_words, words_score=200, last_word_points=1.)
    #     self.assertNotEqual(result, (1., ["hello", "ola"]))
    #     self.assertIn(result[0], self.dict_of_all_words)
    #     self.assertIn(result[1], self.dict_of_all_words.values())

if __name__ == '__main__':
    unittest.main()
