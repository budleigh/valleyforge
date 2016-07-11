import os
import tornado.ioloop
import tornado.web


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        self.write('yo')


def make_app():
    return tornado.web.Application([
        (r'/', IndexHandler),
    ])

if __name__ == '__main__':
    app = make_app()
    app.listen(os.environ.get('PORT', 5000))
    tornado.ioloop.IOLoop.current().start()
