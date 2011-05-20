'''
Created on May 17, 2011

@author: jeden
'''

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from google.appengine.dist import use_library
use_library('django', '1.2')


from google.appengine.ext import webapp
import wsgiref
from handler.async import AsyncHandler
from utils import doRender
from handler.add_request import AddRequestHandler

class MainHandler(webapp.RequestHandler):
    def get(self):
        if not doRender(self, self.request.path):
            doRender(self)
        
def main():
    application = webapp.WSGIApplication([
                                          ('/request/add', AddRequestHandler),
                                          ('/async', AsyncHandler),
                                          ('/.*', MainHandler)],
                                         debug = True)
    wsgiref.handlers.CGIHandler().run(application)
    
if __name__ == '__main__':
    main()
            