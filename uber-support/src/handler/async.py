'''
Created on May 19, 2011

@author: Antonio Bello - Elapsus
'''
from google.appengine.ext import webapp
from handler.retrieve_requestor import RetrieveRequestorCommand
from handler.dashboard_handler import ListResponderRequestsCommand
from handler.list_requests import ListRequestorRequestsCommand

class AsyncHandller(webapp.RequestHandler):
    """ 
        Base handler for asynchronous requests
        Override the _get_routing_table() method to define
        a proper routing table 
    """
    
    def get(self):
        return self.__handleRequest()
        
    def post(self):
        return self.__handleRequest()

    def __handleRequest(self):
        routing_table = self._get_routing_table()
        op = self.request.get('op')
        if op is not None and routing_table.has_key(op):
            command = routing_table[op]
            
            # Execute the command
            runner = command[0](self, command[1])
            return runner.execute()

    def _get_routing_table(self):
        return {}

class RequestorAsyncHandler(AsyncHandller):
    def _get_routing_table(self):
        return {
                'list_requests': [ListRequestorRequestsCommand, {'email': self.request.get('email')}],
                'retrieve_requestor': [RetrieveRequestorCommand, {'email': self.request.get('email')}]
        }
        
class ResponderAsyncHandler(AsyncHandller):
    def _get_routing_table(self):
        return {
                'loadDashboard': [ListResponderRequestsCommand, {}]
                }
    
