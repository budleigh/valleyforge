import threading
import itertools


class PermutationThread(threading.Thread):

    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.socket = socket
        self.words = None
        self.kill = False

    def message(self, message):
        try:
            if self.socket:
                self.socket.write_message(message)
        except:
            self.kill = True

    def run(self):
        for anagram in itertools.permutations(self.words):
            if self.kill:
                break

            anagram = ''.join(list(anagram))
            self.message(anagram)

        self.socket.close()
