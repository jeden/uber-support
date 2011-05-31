'''
Created on May 31, 2011

@author: Antonio Bello - Elapsus
'''
from google.appengine.dist import use_library
use_library('django', '1.2')


from index import MainHandler
from handler.async import AsyncHandler
from handler.add_request import AddRequestHandler
from google.appengine.ext import webapp
import wsgiref

def main():
    application = webapp.WSGIApplication([
                                          ('/req/request/add', AddRequestHandler),
                                          ('/req/async', AsyncHandler),
                                          ('/.*', MainHandler)],
                                         debug = True)
    wsgiref.handlers.CGIHandler().run(application)
    
if __name__ == '__main__':
    main()