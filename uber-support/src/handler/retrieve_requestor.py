'''
Created on May 19, 2011

@author: Antonio Bello - Elapsus
'''
from handler.command import CommandBase
from control.requestor_manager import RequestorManager

class RetrieveRequestor(CommandBase):
    def _execute(self):
        email = self.parameters['email']
        if (email is not None):
            requestor_manager = RequestorManager(email)
            if not requestor_manager.is_new():
                requestor = requestor_manager.get_requestor()
                json = self.jsonize(requestor)
                return self.render_content(json)
