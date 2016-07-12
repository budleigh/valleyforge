import threading


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
        self.socket.write_message(self.words)
        self.socket.close()
