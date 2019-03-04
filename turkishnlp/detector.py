import re
import pickle
import os
from collections import Counter
import sys
import urllib.request


class TurkishNLP:

    def __init__(self):
        """
        Initiating the class.
        """
        self.all_words = None
        self.alphabet = {'a', 'b', 'c', 'ç', 'd', 'e', 'f', 'g', 'ğ', 'h', 'i', 'ı', 'j', 'k', 'l', 'm',
                         'n', 'o', 'ö', 'p', 'q', 'r', 's', 'ş', 't', 'u', 'ü', 'v', 'w', 'x', 'y', 'z', '-',
                                                                                                    ':', '='}
        self.vowels_1 = {'a', 'ı', 'o', 'u'}
        self.vowels_2 = {'e', 'i', 'ö', 'ü'}
        self.vowels = self.vowels_1.union(self.vowels_2)
        self.counted_words = None

    def create_word_set(self):
        """
        Executed at the initiation function
        :return: Returns the words list which is read from the "kelimeler.txt" file
        """
        dir = self.__get_directory()
        if os.path.isfile(dir + "/words.pkl"):
            with open(dir + "/words.pkl", "rb") as f:
                word_set = pickle.load(f)
                self.all_words = word_set
        else:
            raise Exception('You need to download the data first using download() function')

        if os.path.isfile(dir + "/words_counted.pkl"):
            with open(dir + "/words_counted.pkl", "rb") as f_count:
                self.counted_words = pickle.load(f_count)
        else:
            raise Exception('You need to download the data first using download() function')

    def download(self):
        """
        Downloading data to the spesific directory
        :return:
        """
        dir = self.__get_directory()

        if not os.path.exists(dir):
            os.makedirs(dir)

        urllib.request.urlretrieve("http://turkish-nlp.com/datanlp/words.pkl", dir + "/words.pkl")
        urllib.request.urlretrieve("http://turkish-nlp.com/datanlp/words_counted.pkl", dir + "/words_counted.pkl")
        print("Download is successful")

    @staticmethod
    def __get_directory():
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
    def __splits(word):
        return [(word[:i], word[i:])
                for i in range(len(word) + 1)]

    def __detect_it(self, text_array):
        """

        :param text_array: The text array that is going to be checked if it is Turkish or not
        :return: Returns True if it is Turkish and false if not.
        """
        accuracy = 0

        for word in text_array:
            if word in self.all_words and len(word) > 1:
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
        return list(map(self.__correct, word_list))

    def __correct(self, word):
        """

        :param word: Single word to be checked and corrected if needed
        :return: Returns the possible corrected word
        Try to find the best spelling correction for this word
        """
        candidates = (self.__known(self.__edits0(word)) or
                      self.__known(self.__edits1(word)) or
                      self.__known(self.__edits2(word)) or
                      [word])
        return max(candidates, key=self.counted_words.get)

    def __known(self, words):
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
        pairs = self.__splits(word)
        deletes = [a + b[1:] for (a, b) in pairs if b]
        transposes = [a + b[1] + b[0] + b[2:] for (a, b) in pairs if len(b) > 1]
        replaces = [a + c + b[1:] for (a, b) in pairs for c in self.alphabet if b]
        inserts = [a + c + b for (a, b) in pairs for c in self.alphabet]
        return set(deletes + transposes + replaces + inserts)

    def __is_vowel(self, char):
        """

        :param char: Char to be checked
        :return: Return True if char is vowel and False if not
        """
        return char in self.vowels

    def syllabicate(self, word):
        """

        :param word: The word to be syllabicated
        :return: The syllabicated list that contains syllabs
        """
        word = word.lower()
        syllabs = []
        syllab = ""
        last_was_vowel = False
        keep_index = 0
        next_is_vowel = False

        for pos, char in enumerate(word[:-1]):

            next_is_vowel = self.__is_vowel(word[pos + 1])

            if next_is_vowel and syllab and not (last_was_vowel and self.__is_vowel(char)):
                syllabs.append(syllab)
                keep_index = pos
                syllab = ""

            syllab += char

            last_was_vowel = self.__is_vowel(char)

        syllabs.append(word[keep_index:])

        return syllabs

    def syllabicate_sentence(self, sentence):
        """

        :param sentence: The sentence is going to get its words syllabicated
        :return: The syllabicated 2D list
        """
        words_list = self.list_words(sentence)
        return list(map(self.syllabicate, words_list))

    def is_vowel_harmonic(self, word):
        """

        :param word: Takes the word as param
        :return: Returns if it is vowel harmonic
        """
        word = word.lower()
        vowels_1 = [1 if letter in self.vowels_1 else 0 for letter in word if letter in self.vowels]
        return False if 1 in vowels_1 and 0 in vowels_1 else True

    def is_turkish_origin(self, word):
        """

        :param word: Takes the word as param
        :return: Returns if it is Turkish origin
        """
        word = word.lower()
        if not self.is_vowel_harmonic(word) or 'j' in word or 'h' in word:
            return False
        syllabicated = self.syllabicate(word)
        syllab_ = ''.join(syllabicated[1:])
        if len(syllabicated[0]) == 1 and syllabicated[0] not in self.vowels or 'o' in syllab_ or 'ö' in syllab_:
            return False

        return True

    def turkish_origin_accuracy(self, sentence):
        """

        :param sentence: Sentence to be checked
        :return: Returns the accuracy, turkish origin words / words in total
        """
        word_list = self.list_words(sentence)
        turkish_origin_words = [i for i in list(map(self.is_turkish_origin, word_list)) if i]
        return len(turkish_origin_words) / len(word_list)

