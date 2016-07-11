import threading


class PermutationThread(threading.Thread):

    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.socket = socket
        self.words = None

    def run(self):
        self.socket.write_message(self.words)
        self.socket.close()
