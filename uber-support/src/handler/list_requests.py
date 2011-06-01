'''
Created on May 19, 2011

@author: Antonio Bello - Elapsus
'''
from control.requestor_manager import RequestorManager
from control.request_manager import RequestorRequestManager
from handler.command import CommandBase

class ListRequestorRequestsCommand(CommandBase):
    """ Render the list of requests """
    
    def _execute(self):
        email = self.parameters['email']
        requestor_manager = RequestorManager(email)
        request_manager = RequestorRequestManager(requestor_manager.get_requestor().key())
        requests = request_manager.list_requests()
        json = self.jsonize_jqgrid(requests)
        return self.render_content(json)
        
