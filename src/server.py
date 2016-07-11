import os
import tornado.ioloop
import tornado.web
import tornado.websocket
from src.permute import PermutationThread

if not os.environ.get('STATIC_PATH', False):
    os.environ['STATIC_PATH'] = os.path.dirname(os.path.realpath(__file__)) + '/../public'


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('../templates/index.html')


class SocketHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        self.thread = PermutationThread(self)

    def on_message(self, message):
        self.thread.words = message
        self.thread.start()

    def on_close(self):
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
    app.listen(os.environ.get('PORT', 5000))
    tornado.ioloop.IOLoop.current().start()
