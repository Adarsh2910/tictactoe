__author__ = 'ankush'

import cherrypy
import MySQLdb
import json
import game
import os


mysql_credentials = json.load(open('mysql_credentials.json'))

# For thread safety with MySQLdb (http://tools.cherrypy.org/wiki/Databases)
def connect_mysql(thread_index = None): 
    # Create a connection and store it in the current thread 
    cherrypy.thread_data.db = MySQLdb.connect(**mysql_credentials)
    cherrypy.thread_data.db.autocommit(True)        #tried commit() in each function but it didn't work well; so using autocommit(True)

# Tell CherryPy to call "connect" for each thread, when it starts up
cherrypy.engine.subscribe('start_thread', connect_mysql)


class App(object):
    exposed = True

    @cherrypy.tools.allow(methods=['POST','GET'])
    @cherrypy.expose
    def get_optimal_move(self, move_id):
    	cursor = cherrypy.thread_data.db.cursor()
    	try:
    		move = game.get_optimal_move(cursor, move_id=move_id)
    		if not move:
    			pass
    	except (AttributeError, MySQLdb.OperationalError):
    		connect_mysql()
    		cursor = cherrypy.thread_data.db.cursor()
    		move = game.get_optimal_move(cursor, move_id=move_id)
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
    	return str(json.dumps({"move": move}))


    @cherrypy.tools.allow(methods=['GET'])
    @cherrypy.expose
    def play(self):
        return file("tictactoe.html")



if __name__ == '__main__':

    cherrypy.server.socket_host = "0.0.0.0"
    cherrypy.server.socket_port = 8888
    conf = {
            '/static': 
                {
                  'tools.staticdir.on': True,
                  'tools.staticdir.dir': os.path.dirname(os.path.abspath(__file__)) + '/static'
                }
          }
    cherrypy.quickstart(App(), config=conf)
