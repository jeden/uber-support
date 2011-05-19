'''
Created on May 17, 2011

@author: jeden
'''
from google.appengine.ext import webapp
import wsgiref
from control.requestor_manager import RequestorManager
from control.request_manager import RequestManager
import gaesessions
from handler.async import AsyncHandler
from utils import doRender

class Session(gaesessions.Session):
    def is_logged_in(self):
        return self.has_key('user_email')
    
    def register_login(self, email):
        self['user_email'] = email
        
    def get_requestor(self):
        return self.get('requestor', None)
    
    def set_requestor(self, requestor):
        self['requestor'] = requestor
    

class AddRequestHandler(webapp.RequestHandler):
    """ Form to add a new request """

    def __init__(self):
        self.__session = Session()
            
    def get(self):
        doRender(self, 'add_request.html', {
                                            'requestor': self.__session.get_requestor(),
                                            'is_logged_in': self.__session.is_logged_in()})
        
    def post(self):
        email = self.request.get('email')
        category = self.request.get('category')
        subject = self.request.get('subject')
        notes = self.request.get('notes')

        requestor_manager = RequestorManager(email)
        
        if (self.__session.is_logged_in() == False):
            name = self.request.get('name')
            phone = self.request.get('phone')
            company = self.request.get('company')
            
            if requestor_manager.is_new():
                requestor_manager.create_requestor(name, phone, company)
            self.__session.register_login(email)
            self.__session.set_requestor(requestor_manager.get_requestor())
        
        request_manager = RequestManager(requestor_manager.get_requestor())
        request_manager.create_request(category, subject, notes)

        self.get()


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
            