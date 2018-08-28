
import re
import pickle
import os
from collections import Counter
import sys
import urllib.request


class TurkishNLP:

    def __init__(self):
        self.all_words = None
        self.alphabet = 'abcçdefgğhiıjklmnoöpqrsştuüvwxyz-:= '
        self.counted_words = None

    def create_word_set(self):
        """
        Executed at the initiation function
        :return: Returns the words list which is read from the "kelimeler.txt" file
        """
        dir = self.get_directory()
        if os.path.isfile(dir + "/words.pkl"):
            with open(dir + "/words.pkl", "rb") as f:
                word_set = pickle.load(f)
                self.all_words = word_set
        else:
            with open("kelimeler.txt", "r") as file:
                [self.all_words.extend(line.strip().split(",")) for line in file]
            with open("words.pkl", "wb") as f:
                pickle.dump(self.all_words, f)

        if os.path.isfile(dir + "/words_counted.pkl"):
            with open(dir + "/words_counted.pkl", "rb") as f_count:
                self.counted_words = pickle.load(f_count)
        else:
            self.counted_words = Counter(self.all_words)
            with open("words_counted.pkl", "wb") as file_count:
                pickle.dump(self.counted_words, file_count)

    def download(self):
        """
        Downloading data to the spesific directory
        :return:
        """
        dir = self.get_directory()

        if not os.path.exists(dir):
            os.makedirs(dir)

        urllib.request.urlretrieve("http://metehancetinkaya.com/datanlp/words.pkl", dir + "/words.pkl")
        urllib.request.urlretrieve("http://metehancetinkaya.com/datanlp/words_counted.pkl", dir + "/words_counted.pkl")
        print("Succesfully Downloaded")

    @staticmethod
    def get_directory():
        """

        :return: Return the target directory depending on the OS
        """
        if sys.platform == 'win32' and 'APPDATA' in os.environ:
            homedir = os.environ['APPDATA']

            # Otherwise, install in the user's home directory.
        else:
            homedir = os.path.expanduser('~/')
            if homedir == '~/':
                raise ValueError("Could not find a default download directory")

            # append "TRnlpdata" to the home directory
        return os.path.join(homedir, 'TRnlpdata')

    @staticmethod
    def list_words(text):
        """

        :param text: The text that is going to get split into single words
        :return: Returns the words list.
        """
        return re.findall("[a-z,öçüğış]+", text.lower())

    @staticmethod
    def splits(word):
        return [(word[:i], word[i:])
                for i in range(len(word) + 1)]

    def __detect_it(self, text_array):
        """

        :param text_array: The text array that is going to be checked if it is Turkish or not
        :return: Returns True if it is Turkish and false if not.
        """
        accuracy = 0

        for word in text_array:
            if word in self.all_words and len(word) > 2:
                    accuracy += 1

        accuracy = accuracy / len(text_array); print(accuracy)
        return True if accuracy > 0.65 else False

    def is_turkish(self, input_text):
        """

        :param input_text: Whole text to be checked if Turkish as string
        :return: Returns whether if it is Turkish or not, so True or False
        """
        if type(input_text) == str:
            input_text = self.list_words(input_text)
        return self.__detect_it(input_text)

    def auto_correct(self, word_list):
        return list(map(self.correct, word_list))

    def correct(self, word):
        """

        :param word: Single word to be checked and corrected if needed
        :return: Returns the possible corrected word
        Try to find the best spelling correction for this word
        """
        candidates = (self.known(self.__edits0(word)) or
                      self.known(self.__edits1(word)) or
                      self.known(self.__edits2(word)) or
                      [word])
        return max(candidates, key=self.counted_words.get)

    def known(self, words):
        """

        :param words: Word to be checked
        :return: Return the subset of words that allready exists in the dictionary
        """
        return {w for w in words if w in self.counted_words}

    def __edits0(self, word):
        """

        :param word: Word to be corrected
        :return: Return the word itself
        """
        return {word}

    def __edits2(self, word):
        """

        :param word: Word to be corrected
        :return: Return all possibilities of strings that are two edits away from this word
        """
        return {e2 for e1 in self.__edits1(word) for e2 in self.__edits1(e1)}

    def __edits1(self, word):
        """

        :param word: Word to be corrected
        :return: Return all posibilities of strings that are one edit away from this word
        It simply generates all the possibilities with this function.
        """
        pairs = self.splits(word)
        deletes = [a + b[1:] for (a, b) in pairs if b]
        transposes = [a + b[1] + b[0] + b[2:] for (a, b) in pairs if len(b) > 1]
        replaces = [a + c + b[1:] for (a, b) in pairs for c in self.alphabet if b]
        inserts = [a + c + b for (a, b) in pairs for c in self.alphabet]
        return set(deletes + transposes + replaces + inserts)




