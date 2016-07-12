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
        self.queue = queue.Queue()
        self.workers = []

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

    def get_anagram(self):
        anagram = None
        try:
            anagram = self.queue.get_nowait()
        except queue.Empty:
            pass

        return anagram

    def spawn_workers(self):

        def space_pad(string, insert_spaces=0):
            for x in range(insert_spaces):
                string += ' '
            return string

        for x in range(len(self.words)):
            modified = space_pad(self.words, insert_spaces=x)
            self.spawn_worker(self.queue, modified, self.workers)

    def spawn_worker(self, q, string, store):
        worker = SpaceWorker(q, string, self)
        store.append(worker)
        worker.start()

    def cycle(self):
        anagram = self.get_anagram()
        if anagram:
            self.message(anagram)

    def cleanup_workers(self):
        for worker in self.workers:
            if not worker.running:
                self.workers.remove(worker)

        if not self.workers:
            return False  # all done
        return True  # some still working

    def worker_join(self):
        # wait for workers to finish
        while True:
            if self.kill:
                return

            self.cycle()

            if not self.cleanup_workers():
                return

    def run(self):
        self.normalize_words()
        self.spawn_workers()
        self.worker_join()
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

    def parse_anagram(self, anagram):
        words = ''.join(list(anagram))
        words_list = words.split(' ')
        return words, words_list

    def process_anagram(self, anagram):
        anagram, words_list = self.parse_anagram(anagram)
        if anagram in self.seen:
            return anagram, False

        valid = True
        for word in words_list:
            if not self.is_english(word):
                valid = False
                break
        if valid:
            return anagram, True
        else:
            return anagram, False

    def run(self):
        self.running = True
        for anagram in itertools.permutations(self.words):
            if self.parent.kill:
                break

            anagram, valid = self.process_anagram(anagram)
            if valid:
                self.seen.add(anagram)
                self.queue.put(anagram)

        self.running = False

