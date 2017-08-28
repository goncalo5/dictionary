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
        self.up4wrong_words = 50
        # initial n-degree equation
        # (0 = wardest(uniform), 1 = linear, 2 = 2-degree ... inf = easiest(always first word))

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
                print self.args.input_file
            if self.args.input_file:
                self.open_file_txt_and_create_new_file_with_points()
            else:
                self.create_a_new_file_from_scrath()
            if self.args.verbose:
                print self.dict_of_all_words

    def create_a_new_file_from_scrath(self):
        if self.args.verbose:
            print "\ncreate a new file from scrath"
        self.add_new_word()
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

    def check_if_the_points_exist(self, word_points, word):
        if self.args.verbose:
            print "check_if_the_points_exist"
            print word_points, word
            print self.dict_of_all_words
        while True:
            if self.args.verbose:
                print "while true"
            # To avoid deleting an existing word
            try:
                self.dict_of_all_words[word_points]
                if self.args.verbose:
                    print "there are other word with the same key"
                    print self.dict_of_all_words[word_points]
                word_points += 0.0001
            except KeyError:
                if self.args.verbose:
                    print word_points, word
                    print "there are no other word with the same key"
                self.dict_of_all_words[word_points] = word
                break

    def check_if_the_word_exist(self, word):
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

    def add_new_word(self):
        english = raw_input("which word you wanna add?  ")
        # check if that word doesn't already exist
        if self.check_if_the_word_exist(english) is None:
            portuguese = raw_input("what is the solution for that word?  ")
            if portuguese == "q":  # quit
                return
            word = [english, portuguese]
            self.check_if_the_points_exist(word_points=1.0, word=word)
        else:
            self.add_new_word()

    def delete_word(self):
        english = raw_input("which word you wanna delete?  ")
        # check if that word doesn't already exist
        points = self.check_if_the_word_exist(english)
        if points is not None:
            if self.args.verbose:
                print self.dict_of_all_words[points], " deleted"
            del self.dict_of_all_words[points]

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
                if self.args.verbose:
                    print "you answered yes"
                    print type(self.word_points)
                self.word_points = self.word_points * self.increase_rate
                self.words_score = max(self.words_score - self.down4right_words, 0)
            elif check in ["n", "no", "not"]:
                if self.args.verbose:
                    print "you answered no"
                self.word_points = max(self.word_points / self.decreased_rate, 1.0)
                self.words_score += self.up4wrong_words
            elif check in ["a", "add"]:
                if self.args.verbose:
                    print "you answered add"
                self.add_new_word()
            elif check in ["d", "delete"]:
                if self.args.verbose:
                    print "you answered delete"
                self.delete_word()
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

    def run(self):
        if self.args.verbose:
            print self.dict_of_all_words
        # select the first n (random) lower points
        n = len(self.dict_of_all_words)
        self.degree = int(self.words_score / 100)
        if self.args.verbose:
            print "degree: ", self.degree
        for i in xrange(self.degree):
            n = random.randrange(n) + 1
        lower_points = sorted(self.dict_of_all_words)[0:n]
        if self.args.verbose:
            print lower_points
        self.word_points = random.choice(lower_points)
        if self.args.verbose:
            print self.word_points
        word = self.dict_of_all_words[self.word_points]
        self.dict_of_all_words.pop(self.word_points)
        self.clear_screen()
        print "{} ({})".format(word[0], self.word_points)
        raw_input()
        if word[1][0] == " ":
            print word[1][1::]
        else:
            print word[1]
        self.options()
        print self.word_points
        self.check_if_the_points_exist(self.word_points, word)
        if self.args.verbose:
            print self.dict_of_all_words
        self.save_file()
        self.f.close()
        self.run()

Run()
