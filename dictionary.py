import os
import sys
import argparse
import random
import json


class Run(object):
    def __init__(self):
        # file_path_and_name = "/Users/goncalo/Documents/Notes/dicionario.txt"

        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("-v", "--verbose", action='store_true')
        self.parser.add_argument('-i', '--input_file', type=str, nargs=1)
        self.parser.add_argument('-f', '--filename', type=str, nargs=1, default="dicionario.txt")
        self.args = self.parser.parse_args()
        if self.args.verbose:
            print self.args

        self.file_name = self.args.filename[0]
        self.increase_rate = 1.5
        self.decreased_rate = 5.0
        self.number_of_words_sorted = 10

        self.dict_of_all_words = {}
        self.words_score = 500  # 5-degree equation (500/100)
        self.down4right_words = 5
        self.up4wrong_words = 35
        # initial n-degree equation
        # (0 = wardest(uniform), 1 = linear, 2 = 2-degree ... inf = easiest(always first word))
        self.word_points = self.last_word_points = None

        self.try_open_file()
        self.open_file()
        self.run()

    def try_open_file(self):
        try:
            if self.args.verbose:
                print "trying open the file"
            self.open_file()
            if self.args.verbose:
                print "file open with sucess"
        except IOError:
            if self.args.verbose:
                print "can't open the file, need to create new one"
                print "input_file: ", self.args.input_file
            if self.args.input_file:
                self.open_file_txt_and_create_new_file_with_points()
            else:
                self.create_a_new_file_from_scrath()
            if self.args.verbose:
                print self.dict_of_all_words

    def create_a_new_file_from_scrath(self):
        print "\ncreate a new file from scrath"
        while len(self.dict_of_all_words) < 2:
            print "\nplease insert at least 2 word\n\n"
            self.input_new_word()
        self.save_file()

    def open_file(self):
        if self.args.verbose:
            print "\nopen file"
        self.f = open(self.file_name, "r")
        self.dict_of_all_words = json.load(self.f)
        # convert unicode to numbers
        if self.args.verbose:
            print self.dict_of_all_words
        for elem in self.dict_of_all_words:
            value = self.dict_of_all_words[elem]
            self.dict_of_all_words.pop(elem)
            self.dict_of_all_words[float(elem)] = value

    def open_file_txt_and_create_new_file_with_points(self):
        # basicly create a file with a list of words in a txt file
        # format in the existing file: "english_word      translation"

        if self.args.verbose:
            print "open_file_txt_and_create_new_file_with_points"
        input_file = open(self.args.input_file, "r")
        output_file = open(self.file_name, "w")

        i = 1
        for line in input_file:
            line = line.split("  ")
            if line == ["\n"]:
                continue
            line = [line[0], line[-1]]
            # print line,
            self.dict_of_all_words[i] = line
            i += 1

        json.dump(self.dict_of_all_words, output_file)
        input_file.close()
        output_file.close()

    def save_file(self):
        if self.args.verbose:
            print "saving file"
        self.f = open(self.file_name, "w")
        json.dump(self.dict_of_all_words, self.f)

    def check_if_the_points_exist(self, word_points, new=False, last=False):
        if word_points == self.word_points:
            if new:
                return False
            return True
        try:
            if word_points == self.last_word_points:
                if last:
                    return False
                return True
        except AttributeError:
            pass
        if word_points in self.dict_of_all_words:
            return True
        return False

    def create_valide_points(self, word_points, new=False, last=False):
        while self.check_if_the_points_exist(word_points, new=new, last=new):
            word_points += 0.000001
        return word_points

    def check_if_the_word_exist(self, word):
        # return points if the word exist, and False otherwise
        if self.args.verbose:
            print "check if that word already exist", word
        for points in self.dict_of_all_words:
            if self.args.verbose:
                print points, self.dict_of_all_words[points]
            if unicode(word) == self.dict_of_all_words[points][0]:
                print "that word already exist"
                return points
        if self.args.verbose:
            print "that word doesn't exist, will return None"

    def add_new_word(self, new_word, new_word_points, new=False, last=False):
        if self.args.verbose:
            print "\nadd_new_word"
            print self.dict_of_all_words
            print "new_word_points ", new_word_points
            print "new_word ", new_word

        new_word_points = self.create_valide_points(word_points=1.0, new=new, last=last)
        self.dict_of_all_words[new_word_points] = new_word

    def input_new_word(self):
        original_word = raw_input("which word you wanna add?  ")
        original_word = original_word.decode(sys.stdin.encoding)
        # check if that word doesn't already exist
        if self.check_if_the_word_exist(original_word) is None:
            translation = raw_input("what is the solution for that word?  ")
            translation = translation.decode(sys.stdin.encoding)
            if translation == "q":  # quit
                return
            self.add_new_word(new_word=[original_word, translation], new_word_points=1.0)
        else:
            self.input_new_word()

    def delete_word(self, original_word):
        points = self.check_if_the_word_exist(original_word)
        if points is not None:
            if self.args.verbose:
                print self.dict_of_all_words[points], " deleted"
            del self.dict_of_all_words[points]

    def input_word2delete(self):
        original_word = raw_input("which word you wanna delete?  ")
        self.delete_word(original_word)

    def clear_screen(self):
        if not self.args.verbose:
            if os.name == "nt":
                os.system("cls")  # windows
            else:
                os.system("clear")

    def options(self):
        while True:
            if self.args.verbose:
                print "while True"
            options = ["yes", "no", "add", "delete", "quit"]
            for option in options:
                print "[{}]{} ".format(option[0], option[1::]),
            check = raw_input("  ")

            if check in ["y", "yes"]:
                last = self.word_points
                self.word_points = self.word_points * self.increase_rate
                self.words_score = max(self.words_score - self.down4right_words, 0)
                self.word_points = self.word_points + random.random() / 100
                self.dict_of_all_words[self.word_points] = self.dict_of_all_words.pop(last)

                if self.args.verbose:
                    print "you answered yes"
                    print "self.word_points ", self.word_points
                    print "self.words_score", self.words_score

            elif check in ["n", "no", "not"]:
                last = self.word_points
                self.word_points = max(self.word_points / self.decreased_rate, 1.0)
                self.words_score += self.up4wrong_words
                self.word_points = self.word_points + random.random() / 100
                self.dict_of_all_words[self.word_points] = self.dict_of_all_words.pop(last)

                if self.args.verbose:
                    print "you answered no"
                    print "self.word_points ", self.word_points
                    print "self.words_score", self.words_score

            elif check in ["a", "add"]:
                if self.args.verbose:
                    print "you answered add"
                self.input_new_word()
            elif check in ["d", "delete"]:
                if self.args.verbose:
                    print "you answered delete"
                self.input_word2delete()
            elif check in ["q", "quit"]:
                if self.args.verbose:
                    print "you answered quit"
                sys.exit(0)
            else:
                print "please select y (yes) or n (no) if you got the answer right, or q (quit)"
                continue
            break
            if self.args.verbose:
                print "while True end"

    def ensure_that_the_word_does_not_appear_twice_repeated(self):
        if self.args.verbose:
            print "\nensure_that_the_word_does_not_appear_twice_repeated"

        # To ensure that the word does not appear twice repeated
        if self.word_points:
            # save the word to add later
            self.last_word_points = self.word_points
            self.last_word = self.dict_of_all_words[self.last_word_points]
            # remove the word from dict
            # self.dict_of_all_words.pop(self.last_word_points)

    def calc_word_points(self):
        # select the first n (random) lower points
        n = len(self.dict_of_all_words)
        self.degree = int(self.words_score / 100)
        for i in xrange(self.degree):
            n = random.randrange(n) + 1
        lower_points = sorted(self.dict_of_all_words)[0:n]
        self.word_points = random.choice(lower_points)
        if self.word_points == self.last_word_points:
            self.calc_word_points()

        if self.args.verbose:
            print "calc_word_points"
            print "degree: ", self.degree
            print lower_points
            print self.word_points

    def choose_a_word(self):
        if self.args.verbose:
            print "\nchoose_a_word"

        # self.ensure_that_the_word_does_not_appear_twice_repeated()
        self.calc_word_points()
        self.chosen_word = self.dict_of_all_words[self.word_points]
        # self.dict_of_all_words.pop(self.word_points)

    def print_word(self):
        if self.args.verbose:
            print "\nprint_word"

        print "%s  (%s)" % (self.chosen_word[0], self.word_points)

    def print_solution(self):
        if self.args.verbose:
            print "\nprint_solution"

        raw_input()
        if self.chosen_word[1][0] == " ":
            print self.chosen_word[1][1::]
        else:
            print self.chosen_word[1]

    def run(self):
        if self.args.verbose:
            print "\n\nrun"

        self.choose_a_word()
        self.clear_screen()
        self.print_word()
        self.print_solution()
        self.options()
        self.last_word_points = self.word_points

        if self.args.verbose:
            print "chosen_word ", self.chosen_word
            print "word_points ", self.word_points
            print self.dict_of_all_words

        self.save_file()
        self.f.close()
        self.run()

Run()
