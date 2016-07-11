import os
import tornado.ioloop
import tornado.web


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('templates/index.html')


def make_app():
    return tornado.web.Application([
        (r'/', IndexHandler),
        (r'/static/(.*)', tornado.web.StaticFileHandler, {
            'path': os.path.dirname(os.path.realpath(__file__)) + '/static',
        }),
    ])

if __name__ == '__main__':
    app = make_app()
    app.listen(os.environ.get('PORT', 5000))
    tornado.ioloop.IOLoop.current().start()
