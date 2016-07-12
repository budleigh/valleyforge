import threading
import queue
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
        workers = []
        q = queue.Queue()
        for x in range(len(self.words)):
            modified = self.words
            for i in range(x):
                modified += ' '
            sw = SpaceWorker(q, modified, self)
            sw.start()
            workers.append(sw)

        while True:
            if self.kill:
                break

            anagram = None
            try:
                anagram = q.get_nowait()
            except queue.Empty:
                pass
            if anagram:
                self.message(anagram)

            for worker in workers:
                if not worker.running:
                    workers.remove(worker)
            if not workers:
                break

        self.socket.close()


class SpaceWorker(threading.Thread):

    def __init__(self, queue, words, parent):
        threading.Thread.__init__(self)
        self.queue = queue
        self.words = words
        self.parent = parent
        self.seen = set()
        self.running = False

    def is_english(self, word):
        if (len(word) == 1 and word not in list('ia')) or (word not in self.parent.dictionary):
            return False
        return True

    def run(self):
        self.running = True
        for anagram in itertools.permutations(self.words):
            if self.parent.kill:
                break

            anagram = ''.join(list(anagram))
            valid = True
            for word in anagram.split(' '):
                if not self.is_english(word):
                    valid = False
                    break
            if valid:
                if anagram in self.seen:
                    continue
                else:
                    self.seen.add(anagram)
                    self.queue.put(anagram)

        self.running = False

