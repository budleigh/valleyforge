import threading


class PermutationThread(threading.Thread):

    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.socket = socket

    def run(self):
        self.socket.write_message('test permutation')
        self.socket.write_message('test permutation2')
        self.socket.write_message('test permutation3')
        self.socket.close()
