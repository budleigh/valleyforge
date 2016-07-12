import threading
import queue
import itertools


class PermutationThread(threading.Thread):
    """
    A worker with a one-to-one relationship with a socket. The socket is
    sitting in the ioloop of Tornado, but these operations would  still
    be blocking, so we launch a thread for each socket. This normalizes
    the input string, then spawns a bunch of sub-threads that do the actual
    anagram searches based on some variant of the original string with inserted
    spaces.
    """

    def __init__(self, socket, dictionary):
        threading.Thread.__init__(self)
        self.socket = socket
        self.dictionary = dictionary  # english ref from server
        self.words = None
        self.kill = False
        self.seen = set()
        self.queue = queue.Queue()
        self.workers = []
        self.permutations_considered = 0
        self.cycle_count = 0
        # cycle count tracks cycles to send pings at reasonable
        # intervals...-

    def message(self, message):
        # send a message through the socket that spawned it
        try:
            if self.socket:
                self.socket.write_message(message)
        except:
            self.kill = True

    def ping(self, force=False):
        # heroku free instances do this cool thing where they shut
        # down if there are no TCP communication between the server
        # and anyone. so we do this periodic ping to keep it alive
        # piggybacking on that is the 'permutation count'
        message = '--- ' + str(self.permutations_considered)
        if force:
            self.message(message)
            return

        if self.cycle_count == 500:
            self.message(message)
            self.cycle_count = 0
            # reset the cycle count so it doesn't get massive
            # this is sort of unclean, but figure it later

    def normalize_words(self):
        # normalize the string to interact with dictionary
        self.words = self.words.replace(' ', '')
        self.words = self.words.lower()

    def get_anagram(self):
        anagram = None
        # doing this with no blocking on the queue get lets us
        # send more accurate statistics back to the client more
        # often (if needed in future)
        try:
            anagram = self.queue.get_nowait()
        except queue.Empty:
            pass

        return anagram

    def spawn_workers(self):
        # spawn a number of sub-thread workers that handle
        # a different iteration of a 'space-insertion', ie
        # a version of the input string that is tested for
        # anagrams with some extra number of spaces to create
        # the possibility of multiple words

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

    def send_anagram(self):
        # run in the 'mainloop', _join
        # bump cycle here for the ping
        anagram = self.get_anagram()
        if anagram:
            self.message(anagram)

    def cleanup_workers(self):
        # check for idle workers, and get rid of them
        for worker in self.workers:
            if not worker.running:
                self.workers.remove(worker)

        if not self.workers:
            return True  # all done
        return False  # some still working

    def _join(self):
        # PSEUDO_MAINLOOP
        # wait for workers to finish, grab stuff from
        # the queue, write it out, and dump residual
        # once finished
        while True:
            if self.kill:
                return

            # inc cycle, ping and send anagrams (if any)
            self.cycle_count += 1
            self.ping()
            self.send_anagram()

            if self.cleanup_workers():
                self.dump_residual()
                return

    def dump_residual(self):
        # since the workers may finish before the queue
        # is fully handled, we do a second join on the
        # emptying of the queue.
        while not self.queue.empty():
            self.message(self.queue.get())

    def run(self):
        self.normalize_words()
        self.spawn_workers()
        # below blocks until workers are done/q is empty
        self._join()
        self.ping(force=True)  # send a final count
        self.socket.close()


class SpaceWorker(threading.Thread):
    """
    In this situation, each worker thread is handed a particlar modification
    of the socket's string, with some number of spaces inserted (or not) to
    look for anagrams with different numbers of words. The worker handles
    generating the anagrams, testing for English words in it, and sends it
    to the socket's thread-safe write queue if found.
    """

    def __init__(self, queue, words, parent):
        threading.Thread.__init__(self)
        self.queue = queue
        self.words = words
        self.parent = parent
        self.seen = set()
        self.running = False

    def is_english(self, word):
        # the philosophical question here is how to handle one-letter words
        # - also is not sensitive to apostrophes, etc. so no contractions?
        if (len(word) == 1 and word not in list('ia')) or (word not in self.parent.dictionary):
            # here we decide only one letter words i and a are valid
            return False
        return True

    def parse_anagram(self, anagram):
        # make the anagrams returned from itertools useful
        words = ''.join(list(anagram))
        words_list = words.split(' ')
        return words, words_list

    def process_anagram(self, anagram):
        # get an anagram, check the words, return it
        # and the validity of it back to the runloop
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
            # sortof cheating - using the itertools perms to
            # get anagrams - thinking it might be faster.
            if self.parent.kill:
                break

            self.parent.permutations_considered += 1
            # this seems sort of partially thread un-safe?

            anagram, valid = self.process_anagram(anagram)
            if valid:
                # we want to uniqueify the list we send
                self.seen.add(anagram)
                self.queue.put(anagram)

        self.running = False

