import threading
import itertools


class PermutationThread(threading.Thread):

    def __init__(self, socket, dictionary):
        threading.Thread.__init__(self)
        self.socket = socket
        self.dictionary = dictionary  # english ref from server
        self.words = None
        self.kill = False
        self.seen = set()

    def message(self, message):
        try:
            if self.socket:
                self.socket.write_message(message)
        except:
            self.kill = True

    def normalize_words(self):
        # normalize the string to interact with dictionary
        self.words = self.words.replace(' ', '')
        self.words = self.words.lower()

    def run(self):
        self.normalize_words()
        for anagram in itertools.permutations(self.words):
            if self.kill:
                break

            anagram = ''.join(list(anagram))
            if anagram in self.dictionary:
                if anagram in self.seen:
                    continue
                self.message(anagram)
                self.seen.add(anagram)

        self.socket.close()
