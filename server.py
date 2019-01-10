import tornado.ioloop
import tornado.web
import tornado.template
import tornado.websocket
import time
import tornado.ioloop
import json
import logic
#import asyncio.AbstractEventLoop

cl = []
b = logic.Board()
b.play_word( "touzy", 0, 0, logic.RIGHT, "comp" ) #comp
b.play_word( "oy", 0, 1, logic.RIGHT, "Josh" ) #Joshua
b.play_word( "zenith", 3, 0, logic.DOWN, "Jessica" ) #Jessica
b.play_word( "hit", 3, 5, logic.RIGHT, "Hannah" ) #Hannah
b.play_word( "diether", 0, 4, logic.RIGHT, "comp" )#comp

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render( "index.html" )

#pulling from https://github.com/hiroakis/tornado-websocket-example/blob/master/app.py
class SocketHandler(tornado.websocket.WebSocketHandler):
    # def check_origin(self, origin):
    #     return True

    def long_compute_gen( self, number ):
        for i in range( number ):
            time.sleep( 5 )
            yield i

    # def long_compute( self, something ):
    #     for _ in range( 10 ):
    #         time.sleep( .5 )
    #     return 2

    async def on_message(self, message):
        print(u"You said: " + message)
        self.write_message( json.dumps( [ "played_spaces",  b.get_played_spaces() ] ) )
        self.write_message( json.dumps( [ "special_squares", b.special_squares ] ) )
        

        # #computed = await AbstractEventLoop.run_in_executor(None, long_compute, None)
        # g = self.long_compute_gen( 10 )

        # def g_user():
        #     try:
        #         value = next(g)
        #     except StopIteration:
        #         value = -1
        #     return value

        # value = await tornado.ioloop.IOLoop.current().run_in_executor(None, g_user )
        # while value != -1:
        #     self.write_message( u"the result is " + str(value) )
        #     value = await tornado.ioloop.IOLoop.current().run_in_executor(None, g_user )



    def open(self):
        if self not in cl:
            cl.append(self)

    def on_close(self):
        if self in cl:
            cl.remove(self)

if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r'/ws', SocketHandler),
        (r'/(processing.js)', tornado.web.StaticFileHandler, {'path': './'}),
    ], debug=True)
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()