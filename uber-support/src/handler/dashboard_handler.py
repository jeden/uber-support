'''
Created on May 31, 2011

@author: Antonio Bello - Elapsus
'''
from google.appengine.ext import webapp
from utils.template import render_template
from handler.command import CommandBase
from control.request_manager import ResponderRequestManager
from model.request_entity import RequestStatus

class DashboardHandler(webapp.RequestHandler):
    def get(self):
        render_template(self, 'responder_dashboard.html', {
                                                           })
        
class ListResponderRequestsCommand(CommandBase):
    """ Render the list of requests """
    
    def _execute(self):
        try:
            status = self.parameters['status']
        except KeyError:
            status = RequestStatus.NONE
            
        try:
            sort_order = self.parameters['sort_by'].upper()
        except KeyError:
            sort_order = None
        
        try:
            sort_descending = self.parameters['sort_desc']
        except KeyError:
            sort_descending = False
        
        request_manager = ResponderRequestManager()
        requests = request_manager.list_requests(status = status, sort_by = sort_order, sort_descending = sort_descending)
        json = self.jsonize_jqgrid(requests)
        return self.render_content(json)
        
