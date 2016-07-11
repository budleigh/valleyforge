import threading


class PermutationThread(threading.Thread):

    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.socket = socket

    def run(self):
        self.socket.write_message('inside permutation thread')
        self.socket.close()
