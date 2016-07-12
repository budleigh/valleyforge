import os
import nltk
import tornado.ioloop
import tornado.web
import tornado.websocket

from src.server.permute import PermutationThread

if not os.environ.get('STATIC_PATH', False):
    os.environ['STATIC_PATH'] = os.path.dirname(os.path.realpath(__file__)) + '/../../public'

english = set(w.lower() for w in nltk.corpus.words.words())
# set the above so we dont load it again for every open socket


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('../templates/index.html')


class SocketHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        # tornado requires this for any sockets to work
        # im sure i should be doing something here but..
        return True

    def open(self):
        self.thread = PermutationThread(self, english)

    def on_message(self, message):
        # the message contains the query from the client
        # this happens every time they hit enter in the
        # search bar
        self.thread.words = message
        self.thread.start()

    def on_close(self):
        try:
            self.thread.kill = True
        except AttributeError:
            # worker is already dead
            pass


def make_app():
    return tornado.web.Application([
        (r'/', IndexHandler),
        (r'/socket/', SocketHandler),
        (r'/static/(.*)', tornado.web.StaticFileHandler, {
            'path': os.environ.get('STATIC_PATH'),
        }),
    ])

if __name__ == '__main__':
    app = make_app()
    # heroku stores ports in the environment
    # we use 5000 as a default for local builds
    app.listen(os.environ.get('PORT', 5000))
    tornado.ioloop.IOLoop.current().start()
