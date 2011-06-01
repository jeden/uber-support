'''
Created on May 17, 2011

@author: jeden
'''

from google.appengine.dist import use_library
use_library('django', '1.2')




from google.appengine.ext import webapp
import wsgiref
from utils.template import render_template

class MainHandler(webapp.RequestHandler):
    def get(self):
        if not render_template(self, self.request.path):
            render_template(self)

def main():
    application = webapp.WSGIApplication([
                                          ('/.*', MainHandler)],
                                         debug = True)
    wsgiref.handlers.CGIHandler().run(application)
    
if __name__ == '__main__':
    main()