'''
Created on May 31, 2011

@author: Antonio Bello - Elapsus
'''
from google.appengine.ext import webapp
from utils.template import render_template
from handler.command import CommandBase
from control.request_manager import ResponderRequestManager

class DashboardHandler(webapp.RequestHandler):
    def get(self):
        render_template(self, 'responder_dashboard.html', {
                                                           })
        
class ListResponderRequestsCommand(CommandBase):
    """ Render the list of requests """
    
    def _execute(self):
        request_manager = ResponderRequestManager()
        requests = request_manager.list_requests()
        json = self.jsonize_jqgrid(requests)
        return self.render_content(json)
        
