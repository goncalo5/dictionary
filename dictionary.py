import os
import sys
import argparse
import time
import random
import json


class Run(object):
    def __init__(self):
        if __name__ == '__main__':
            self.initiate_settings()
            self.try_open_file()
            self.open_file()
            self.run()

    def initiate_settings(self):
        # file_path_and_name = "/Users/goncalo/Documents/Notes/dicionario.txt"
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("-v", "--verbose", action='store_true')
        self.parser.add_argument('-i', '--input_file', type=str, nargs=1)
        self.parser.add_argument('-f', '--filename', type=str, nargs=1, default="dicionario.txt")
        self.args = self.parser.parse_args()
        if __name__ == '__main__' and self.args.verbose:
            print self.args

        self.file_name = self.args.filename[0]
        self.increase_rate = 1.5
        self.decreased_rate = 5.0
        self.number_of_words_sorted = 10

        self.dict_of_all_words = {}
        self.words_score = 500  # 5-degree equation (500/100)
        self.down4right_words = 50  # self.words_score will be divided by
        # increment = self.up4wrong_words_a / ( self.word_points + self.up4wrong_words_b)
        self.up4wrong_words_a = 10000.
        self.up4wrong_words_b = 20.
        # initial n-degree equation
        # (0 = wardest(uniform), 1 = linear, 2 = 2-degree ... inf = easiest(always first word))
        self.word_points = self.last_word_points = None

    # File
    def try_open_file(self):
        try:
            if __name__ == '__main__' and self.args.verbose:
                print "trying open the file"
            self.open_file()
            if __name__ == '__main__' and self.args.verbose:
                print "file open with sucess"
        except IOError:
            if __name__ == '__main__' and self.args.verbose:
                print "can't open the file, need to create new one"
                print "input_file: ", self.args.input_file
            if self.args.input_file:
                self.open_file_txt_and_create_new_file_with_points()
            else:
                self.create_a_new_file_from_scrath()
            if __name__ == '__main__' and self.args.verbose:
                print self.dict_of_all_words

    def create_a_new_file_from_scrath(self):
        print "\ncreate a new file from scrath"
        while len(self.dict_of_all_words) < 2:
            print "\nplease insert at least 2 word\n\n"
            self.option_a()  # option add
        self.save_file()

    def open_file(self):
        if __name__ == '__main__' and self.args.verbose:
            print "\nopen file"
        self.f = open(self.file_name, "r")
        self.dict_of_all_words = json.load(self.f)
        # convert unicode to numbers
        if __name__ == '__main__' and self.args.verbose:
            print self.dict_of_all_words
        for elem in self.dict_of_all_words:
            value = self.dict_of_all_words[elem]
            self.dict_of_all_words.pop(elem)
            self.dict_of_all_words[float(elem)] = value

    def open_file_txt_and_create_new_file_with_points(self):
        # basicly create a file with a list of words in a txt file
        # format in the existing file: "english_word      translation"

        if __name__ == '__main__' and self.args.verbose:
            print "open_file_txt_and_create_new_file_with_points"
        input_file = open(self.args.input_file, "r")
        output_file = open(self.file_name, "w")

        i = 1
        for line in input_file:
            line = line.split("  ")
            if line == ["\n"]:
                continue
            if line[-1][0] == " ":
                line = [line[0], line[-1]][1::]
            else:
                line = [line[0], line[-1]]
            line = [line[0], line[-1]]
            # print line,
            self.dict_of_all_words[i] = line
            i += 1

        json.dump(self.dict_of_all_words, output_file)
        input_file.close()
        output_file.close()

    def save_file(self):
        if __name__ == '__main__' and self.args.verbose:
            print "saving file"
        self.f = open(self.file_name, "w")
        json.dump(self.dict_of_all_words, self.f)

    def check_if_the_points_exist(self, word_points, dictionary=None):
        if dictionary is None:
            dictionary = self.dict_of_all_words
        if word_points in dictionary:
            return True
        return False

    def create_valide_points(self, word_points, dictionary=None):
        if dictionary is None:
            dictionary = self.dict_of_all_words
        while self.check_if_the_points_exist(word_points, dictionary):
            word_points += random.random() / 1000
        return word_points

    def check_if_the_word_exist(self, word, dictionary=None):
        # return points if the word exist, and None otherwise
        if dictionary is None:
            dictionary = self.dict_of_all_words
        if __name__ == '__main__' and self.args.verbose:
            print "check if that word already exist", word
        for points in dictionary:
            if __name__ == '__main__' and self.args.verbose:
                print points, dictionary[points]
            if unicode(word) == dictionary[points][0]:
                if __name__ == '__main__' and self.args.verbose:
                    print "\n\nthat word already exist"
                return points
        if __name__ == '__main__' and self.args.verbose:
            print "that word doesn't exist, will return None"

    def add_new_word(self, new_word, new_word_points, dictionary=None):
        if __name__ == '__main__' and self.args.verbose:
            print "\nadd_new_word"
            print self.dict_of_all_words
            print "new_word_points ", new_word_points
            print "new_word ", new_word

        if dictionary is None:
            dictionary = self.dict_of_all_words
        if not self.check_if_the_word_exist(new_word[0], dictionary):
            new_word_points = self.create_valide_points(
                word_points=new_word_points, dictionary=dictionary)
            dictionary[new_word_points] = new_word

    def delete_word(self, original_word, dictionary=None):
        if not dictionary:
            dictionary = self.dict_of_all_words
        points = self.check_if_the_word_exist(original_word, dictionary)
        if points is not None:
            if __name__ == '__main__' and self.args.verbose:
                print dictionary[points], " deleted"
            del dictionary[points]

    def clear_screen(self):
        if not self.args.verbose:
            if os.name == "nt":
                os.system("cls")  # windows
            else:
                os.system("clear")

    # Options
    def option_y(self):
        self.words_score -= self.words_score / self.down4right_words

        last = self.word_points
        self.word_points = self.word_points * self.increase_rate
        # to ensure there is no overlap of words
        while self.word_points in self.dict_of_all_words:
            self.word_points += random.random() / 1000
        self.dict_of_all_words[self.word_points] = self.dict_of_all_words.pop(last)

        if __name__ == '__main__' and self.args.verbose:
            print "you answered yes"
            print "self.word_points ", self.word_points
            print "self.words_score", self.words_score

    def option_n(self):
        self.words_score +=\
            float(self.up4wrong_words_a) / (self.words_score + self.up4wrong_words_b)

        last = self.word_points
        self.word_points = max(self.word_points / self.decreased_rate, 1.0)
        # to ensure there is no overlap of words
        while self.word_points in self.dict_of_all_words:
            self.word_points += random.random() / 1000
        self.dict_of_all_words[self.word_points] = self.dict_of_all_words.pop(last)

        if __name__ == '__main__' and self.args.verbose:
            print "you answered no"
            print "self.word_points ", self.word_points
            print "self.words_score", self.words_score
            print "self.up4wrong_words_a", self.up4wrong_words_a
            print "self.up4wrong_words_b", self.up4wrong_words_b
            print "self.up4wrong_words_a / (self.words_score + self.up4wrong_words_b)"
            print self.up4wrong_words_a / (self.words_score + self.up4wrong_words_b)

    def option_a(self):
        if __name__ == '__main__' and self.args.verbose:
            print "you answered add"
        original_word = raw_input("\n\nwhich word you wanna add?  ").decode(sys.stdin.encoding)
        # check if that word doesn't already exist and give the points in case of existing
        original_word_exist = self.check_if_the_word_exist(original_word)
        if not original_word_exist:
            translation = raw_input("what is the solution for that word?  ").decode(sys.stdin.encoding)
            if translation == "q":  # quit
                return
            self.add_new_word(new_word=[original_word, translation], new_word_points=1.0)
        else:
            translation = self.dict_of_all_words[original_word_exist][1]
            print "\nthe word %s already exists, with the translation: %s" % (original_word, translation)
            time.sleep(5)

    def option_m(self):
        if __name__ == '__main__' and self.args.verbose:
            print "you answered modify"
        word2modify = raw_input("\n\nwhich word you wanna modify the solution?  ")
        word2modify_points = self.check_if_the_word_exist(word2modify)
        if word2modify_points:
            translation = self.dict_of_all_words[word2modify_points][1]
            print "\n\nthe word %s already exists, with the translation: %s" % (word2modify, translation)
            translation = raw_input("\nwhat is the new solution for that word?  ").decode(sys.stdin.encoding)
            self.dict_of_all_words[word2modify_points][1] = translation
        else:
            print "that word don't exist, please insert a word that already exist or add new one"
            self.print_menu()

    def option_d(self):
        if __name__ == '__main__' and self.args.verbose:
            print "you answered delete"
        original_word = raw_input("which word you wanna delete?  ")
        self.delete_word(original_word)

    def option_q(self):
        if __name__ == '__main__' and self.args.verbose:
            print "you answered quit"
        sys.exit(0)

    def print_menu(self):
        while True:
            if __name__ == '__main__' and self.args.verbose:
                print "while True"
            options = ["yes", "no", "add", "modify", "delete", "quit"]
            menu = "\n"
            for option in options:
                menu += "[{}]{} ".format(option[0], option[1::])
            print menu,
            choice = raw_input("  ").strip()
            if __name__ == '__main__' and self.args.verbose:
                print "choice: ", choice
                print "len(choice) != 1 ", len(choice) != 1
                print "choice not in options", choice not in options
            erro_msg = "\n\nI don't understand your answer, please select one of the below posiblilities"
            if len(choice) != 1 and choice not in options:
                print erro_msg
                continue
            try:
                if __name__ == '__main__' and self.args.verbose:
                    print '"option_" + choice[0]', "option_" + choice[0]
                getattr(self, "option_" + choice[0])()
            except AttributeError:
                print erro_msg
                continue
            break

    def calc_word_points(self, dictionary=None, words_score=None):
        if not dictionary:
            dictionary = self.dict_of_all_words
        if not words_score:
            words_score = self.words_score
        # select the first n (random) lower points
        while True:
            n = len(dictionary)
            degree = int(words_score / 100)
            for i in xrange(degree):
                n = random.randrange(n) + 1
            lower_points = sorted(dictionary)[0:n]
            self.word_points = random.choice(lower_points)
            if self.word_points != self.last_word_points:
                break

        if __name__ == '__main__' and self.args.verbose:
            print "calc_word_points"
            print "degree: ", degree
            print lower_points
            print self.word_points

    def choose_a_word(self):
        if __name__ == '__main__' and self.args.verbose:
            print "\nchoose_a_word"

        self.calc_word_points()
        self.chosen_word = self.dict_of_all_words[self.word_points]

    def print_word_and_solution(self):
        if __name__ == '__main__' and self.args.verbose:
            print "\print_word_and_solution"

        print "%s  (%s points)  words: %s   score: %s"\
            % (self.chosen_word[0], int(self.word_points),
                len(self.dict_of_all_words), int(self.words_score))
        raw_input()
        print self.chosen_word[1]

    def run(self):
        while True:
            if __name__ == '__main__' and self.args.verbose:
                print "\n\nrun"

            self.choose_a_word()
            self.clear_screen()
            self.print_word_and_solution()
            self.print_menu()
            self.last_word_points = self.word_points

            if __name__ == '__main__' and self.args.verbose:
                print "chosen_word ", self.chosen_word
                print "word_points ", self.word_points
                print self.dict_of_all_words

            self.save_file()
            self.f.close()
        # self.run()

if __name__ == '__main__':
    Run()
