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
# b.play_word( "touzy", 0, 0, logic.RIGHT, "comp" ) #comp
# b.play_word( "oy", 0, 1, logic.RIGHT, "Josh" ) #Joshua
# b.play_word( "zenith", 3, 0, logic.DOWN, "Jessica" ) #Jessica
# b.play_word( "hit", 3, 5, logic.RIGHT, "Hannah" ) #Hannah
# b.play_word( "diether", 0, 4, logic.RIGHT, "comp" )#comp

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render( "index.html" )

#pulling from https://github.com/hiroakis/tornado-websocket-example/blob/master/app.py
class SocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True


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

    word_finder = None
    word_finder_letters = None
    def find_next_word( self, letters ):
        if self.word_finder is None or self.word_finder_letters != letters:
            self.word_finder_letters = letters
            self.word_finder = b.find_word_gen( letters )

        try:
            next_find = next(self.word_finder)
        except StopIteration:
            next_find = None

        return next_find


    async def on_message(self, message):
        print(u"You said: " + message)
        command = json.loads( message )
    
        if command[0] == "play_word":
            try:
                b.play_word( command[1]["word"], int( command[1]["x"] ), int( command[1]["y"] ), int( command[1]["direction"] ) )
            except Exception as ex:
                self.write_message( json.dumps( ["alert", "Error: " + str(ex)]) )

            for c in cl:
                c.write_message( json.dumps( [ "played_spaces",  b.get_played_spaces() ] ) )
        elif command[0] == "find_word":
            self.word_finder = None
            finding_result = await tornado.ioloop.IOLoop.current().run_in_executor(None,self.find_next_word, command[1]["letters"])
            while finding_result is not None:
                self.write_message( json.dumps( finding_result ) )
                finding_result = await tornado.ioloop.IOLoop.current().run_in_executor(None,self.find_next_word, command[1]["letters"])
        else:
            print( "Received command " + command[0] )
        

      



    def open(self):
        if self not in cl:
            cl.append(self)

        self.write_message( json.dumps( [ "played_spaces",  b.get_played_spaces() ] ) )
        self.write_message( json.dumps( [ "special_squares", b.special_squares ] ) )

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