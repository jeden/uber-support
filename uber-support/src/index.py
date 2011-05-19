'''
Created on May 17, 2011

@author: jeden
'''
from google.appengine.ext import webapp
import wsgiref
import os
from google.appengine.ext.webapp import template
from control.requestor_manager import RequestorManager
from control.request_manager import RequestManager
import gaesessions

class Session(gaesessions.Session):
    def is_logged_in(self):
        return self.has_key('user_email')
    
    def register_login(self, email):
        self['user_email'] = email
        
    def get_requestor(self):
        return self.get('requestor', None)
    
    def set_requestor(self, requestor):
        self['requestor'] = requestor
    

def doRender(handler, template_page = 'index.html', values = {}):
    path = os.path.join(os.path.dirname(__file__), 'templates/' + template_page)
    
    if not os.path.isfile(path):
        return False
    
    # Make a copy of the dictionary and add the path
    map = dict(values)
    map['path'] = handler.request.path
    
    html = template.render(path, map)
    handler.response.out.write(html)
    
    return True
    
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

class ListRequestsHandler(webapp.RequestHandler):
    """ List of existing requests """
    
    def get(self):
        requestor_manager = RequestorManager('test@test.com')
        request_manager = RequestManager(requestor_manager.get_requestor().key())
        requests = request_manager.list_requests()
        doRender(self, 'list_requests.html', {
                                              'requests_list': requests
                                              })

class VerifyRequestorHandler(webapp.RequestHandler):
    
    def __init__(self):
        self.__session = Session()
    
    def post(self):
        email = self.request.get('email')
        if (email is not None):
            requestor = RequestorManager(email)
            if (requestor.is_new() is not None):
                self.__session.register_login(email)
                self.__session.set_requestor(requestor.get_requestor())
                
            

class MainHandler(webapp.RequestHandler):
    def get(self):
        if not doRender(self, self.request.path):
            doRender(self)
        
def main():
    application = webapp.WSGIApplication([
                                          ('/request/add', AddRequestHandler),
                                          ('/request/list', ListRequestsHandler),
                                          ('/requestor/verify', VerifyRequestorHandler),
                                          ('/.*', MainHandler)],
                                         debug = True)
    wsgiref.handlers.CGIHandler().run(application)
    
if __name__ == '__main__':
    main()
            