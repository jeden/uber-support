'''
Created on May 31, 2011

@author: Antonio Bello - Elapsus
'''

from google.appengine.dist import use_library
use_library('django', '1.2')


from index import MainHandler
from handler.dashboard_handler import DashboardHandler
from handler.edit_request_handler import EditRequestHandler, ViewRequestHandler
from handler.async import ResponderAsyncHandler

from google.appengine.ext import webapp
import wsgiref


def main():
    application = webapp.WSGIApplication([
                                          ('/res/dashboard', DashboardHandler),
                                          ('/res/request/edit/([^/]+)/([^/]+)', EditRequestHandler),
                                          ('/res/async/request/view/([^/]+)/([^/]+)', ViewRequestHandler),
                                          ('/res/async', ResponderAsyncHandler),
                                          ('/.*', MainHandler)],
                                         debug = True)
    wsgiref.handlers.CGIHandler().run(application)
    
if __name__ == '__main__':
    main()