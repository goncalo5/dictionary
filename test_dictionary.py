#!/usr/bin/python
import unittest
import dictionary


class TestWizard(unittest.TestCase):

    def setUp(self):
        self.run = dictionary.Run()
        self.dict_of_all_words = {
            1.: ["hello", "ola"], 25.69675451079: ["hero", "her\u00f3i"],
            2.: ["cart", "carrinho/carro\u00e7a"], 30.26948287757: ["ship", "barco/navio"],
            }

    def test_check_if_the_points_exist(self):
        # print a.dict_of_all_words
        result = self.run.check_if_the_points_exist(2., self.dict_of_all_words)
        self.assertEqual(result, True)
        result = self.run.check_if_the_points_exist(2.1, self.dict_of_all_words)
        self.assertEqual(result, False)
        result = self.run.check_if_the_points_exist(25.69675451079, self.dict_of_all_words)
        self.assertEqual(result, True)
        result = self.run.check_if_the_points_exist(25.696754510795, self.dict_of_all_words)
        self.assertEqual(result, False)
        result = self.run.check_if_the_points_exist(25.6967545107, self.dict_of_all_words)
        self.assertEqual(result, False)

    def test_create_valide_points(self):
        result = self.run.create_valide_points(10., self.dict_of_all_words)
        self.assertEqual(result, 10.)
        result = self.run.create_valide_points(2., self.dict_of_all_words)
        self.assertGreater(result, 2.)
        result = self.run.create_valide_points(30.26948287757, self.dict_of_all_words)
        self.assertGreater(result, 30.26948287757)

        result = self.run.create_valide_points(30.26948287757, self.dict_of_all_words)
        result = round(result, 2)
        self.assertEqual(result, 30.27)

    def test_check_if_the_word_exist(self):
        result = self.run.check_if_the_word_exist("hero", self.dict_of_all_words)
        self.assertEqual(result, 25.69675451079)
        result = self.run.check_if_the_word_exist("cart", self.dict_of_all_words)
        self.assertEqual(result, 2.)
        result = self.run.check_if_the_word_exist("unknown", self.dict_of_all_words)
        self.assertEqual(result, None)

    def test_add_new_word(self):
        new_dict = self.dict_of_all_words.copy()
        result = self.run.add_new_word(
            new_word=["hello", "ola"], new_word_points=1., dictionary=new_dict)
        self.assertEqual(result, None)

        new_dict = self.dict_of_all_words.copy()
        self.run.add_new_word(
            new_word=["unknown", "nao sei"], new_word_points=1., dictionary=new_dict)
        new_dict.update({1.: ["unknown", "nao sei"]})
        self.assertEqual(new_dict, new_dict)

        new_dict = self.dict_of_all_words.copy()
        self.run.add_new_word(
            new_word=["unknown", "nao sei"], new_word_points=25.69675451079,
            dictionary=new_dict)
        self.assertEqual(len(new_dict), len(self.dict_of_all_words) + 1)

    def test_delete_word(self):
        new_dict = self.dict_of_all_words.copy()
        self.run.delete_word(original_word="hello", dictionary=new_dict)
        self.assertEqual(len(new_dict), len(self.dict_of_all_words) - 1)

        new_dict = self.dict_of_all_words.copy()
        self.run.delete_word(original_word="unknown", dictionary=new_dict)
        self.assertEqual(len(new_dict), len(self.dict_of_all_words))

    def test_calc_word_points(self):
        result = self.run.calc_word_points(
            dictionary=self.dict_of_all_words, words_score=200, last_word_points=2.)
        self.assertNotEqual(result, 2.)
        self.assertIn(result, self.dict_of_all_words)
        result = self.run.calc_word_points(
            dictionary=self.dict_of_all_words, words_score=800, last_word_points=1.)
        self.assertNotEqual(result, 1.)
        self.assertIn(result, self.dict_of_all_words)
        result = self.run.calc_word_points(
            dictionary=self.dict_of_all_words, words_score=50, last_word_points=30.26948287757)
        self.assertNotEqual(result, 30.26948287757)
        self.assertIn(result, self.dict_of_all_words)

    def test_choose_a_word(self):
        result = self.run.choose_a_word(
            dictionary=self.dict_of_all_words, words_score=200, last_word_points=1.)
        self.assertNotEqual(result, (1., ["hello", "ola"]))
        self.assertIn(result[0], self.dict_of_all_words)
        self.assertIn(result[1], self.dict_of_all_words.values())

if __name__ == '__main__':
    unittest.main()
