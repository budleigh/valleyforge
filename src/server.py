import os
import tornado.ioloop
import tornado.web
import tornado.websocket


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('../templates/index.html')


class SocketHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        print('connected')

    def on_message(self, message):
        pass

    def on_close(self):
        pass


def make_app():
    return tornado.web.Application([
        (r'/', IndexHandler),
        (r'/socket/', SocketHandler),
        (r'/static/(.*)', tornado.web.StaticFileHandler, {
            'path': os.path.dirname(os.path.realpath(__file__)) + '../static',
        }),
    ])

if __name__ == '__main__':
    app = make_app()
    app.listen(os.environ.get('PORT', 5000))
    tornado.ioloop.IOLoop.current().start()
