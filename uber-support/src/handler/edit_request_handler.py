'''
Created on Jun 3, 2011

@author: Antonio Bello - Elapsus
'''
from google.appengine.ext import webapp
from utils.template import render_template
from utils import sequential_list_to_map
from control.request_manager import ResponderRequestManager
from google.appengine.ext.db import djangoforms
from model.request_entity import RequestEntity

class RequestForm(djangoforms.ModelForm):
    class Meta:
        model = RequestEntity
        
    def __init__(self, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs)

class _RequestHandler(webapp.RequestHandler):
    def initialize(self, request, response):
        super(_RequestHandler, self).initialize(request, response)
        self._request_manager = ResponderRequestManager()

    def _load_request(self, *args):
        # Extract the request id from the path
        path_params = sequential_list_to_map(args)
        if path_params.has_key('id'):
            id = path_params['id']
            self._request = self._request_manager.find_request(id)
        else:
            self._request = None
        
class EditRequestHandler(_RequestHandler):
    
    def get(self, *args, **kwargs):
        self._load_request(*args)
        
        request_form = kwargs.has_key('request_form') and kwargs['request_form'] or RequestForm()
        
        # Extract the request id from the path
        if self._request is not None:
            request_form = RequestForm(instance = self._request)
        else:
            request_form = None
            
        render_template(self, 'edit_request.html', {
                                            'request_form': request_form,
                                            'request_id': self._request.key().id(),
                                        });
                                    
    
class ViewRequestHandler(_RequestHandler):
    def get(self, *args, **kwargs):
        self._load_request(*args)
        render_template(self, 'panel_request_view.html', {
                                            'can_view': self._request is not None,
                                            'request_id': self._request.key().id(),
                                            'request': self._request
                                        });
