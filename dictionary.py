import os
import argparse
import random
import json


class Run(object):
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("-v", "--verbose", action='store_true')
        self.args = self.parser.parse_args()

        self.file_path_and_name = "/Users/goncalo/Documents/Notes/dicionario.txt"
        self.new_file_name = "dicionario.txt"
        self.increase_rate = 1.5
        self.decreased_rate = 5.0
        self.number_of_words_sorted = 10

        self.dict_of_all_words = {}

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
            self.open_file_txt_and_create_new_file_with_points()
            if self.args.verbose:
                print self.dict_of_all_words
            if self.args.verbose:
                print self.dict_of_all_words

    def open_file(self):
        if self.args.verbose:
            print "\nopen file"
        self.f = open(self.new_file_name, "r")
        self.dict_of_all_words = json.load(self.f)
        # convert unicode to numbers
        if self.args.verbose:
            print self.dict_of_all_words
        for elem in self.dict_of_all_words:
            value = self.dict_of_all_words[elem]
            self.dict_of_all_words.pop(elem)
            self.dict_of_all_words[float(elem)] = value

    def open_file_txt_and_create_new_file_with_points(self):
        input_file = open(self.file_path_and_name, "r")
        output_file = open(self.new_file_name, "w")

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
        self.f = open(self.new_file_name, "w")
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

    def add_new_word(self):
        english = raw_input("which word you wanna add?  ")
        portuguese = raw_input("what is the solution for that word?  ")
        word = [english, portuguese]
        self.check_if_the_points_exist(word_points=1.0, word=word)

    def run(self):
        if self.args.verbose:
            print self.dict_of_all_words
        sorted(self.dict_of_all_words)
        lower_points = sorted(self.dict_of_all_words)[0:self.number_of_words_sorted]
        if self.args.verbose:
            print lower_points
        word_points = random.choice(lower_points)
        if self.args.verbose:
            print word_points
        word = self.dict_of_all_words[word_points]
        self.dict_of_all_words.pop(word_points)
        if not self.args.verbose:
            os.system('clear')
        print "{} ({})".format(word[0], word_points)
        raw_input()
        if word[1][0] == " ":
            print word[1][1::]
        else:
            print word[1]
        check = raw_input("right? [y]es or [n]o [a]dd [q]uit  ")
        if check in ["y", "yes"]:
            if self.args.verbose:
                print "you answered yes"
                print type(word_points)
            word_points = word_points * self.increase_rate
        elif check in ["n", "no", "not"]:
            if self.args.verbose:
                print "you answered no"
            word_points = max(word_points / self.decreased_rate, 1.0)
        elif check in ["a", "add"]:
            if self.args.verbose:
                print "you answered add"
            self.add_new_word()
        elif check in ["q", "quit"]:
            return
        else:
            print "please select y (yes) or n (no) if you got the answer right, or e (exit)"
        print word_points
        self.check_if_the_points_exist(word_points, word)
        if self.args.verbose:
            print self.dict_of_all_words
        self.save_file()
        self.f.close()
        self.run()

Run()
