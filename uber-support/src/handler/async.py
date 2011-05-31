'''
Created on May 19, 2011

@author: Antonio Bello - Elapsus
'''
from google.appengine.ext import webapp
from handler.list_requests import ListRequestsCommand
from handler.retrieve_requestor import RetrieveRequestor

class AsyncHandler(webapp.RequestHandler):
    """ Handler for asynchronous requests """
    
    def get(self):
        return self.__handleRequest()
        
    def post(self):
        return self.__handleRequest()
        
    def __handleRequest(self):
        routing_table = {
                         'list_requests': [ListRequestsCommand, {'email': self.request.get('email')}],
                         'retrieve_requestor': [RetrieveRequestor, {'email': self.request.get('email')}]
                    }
        
        op = self.request.get('op')
        if op is not None and routing_table.has_key(op):
            command = routing_table[op]
            
            # Execute the command
            runner = command[0](self, command[1])
            return runner.execute()
                
