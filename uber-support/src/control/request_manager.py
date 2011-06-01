'''
Created on May 14, 2011

@author: Antonio Bello - Elapsus
'''
from model.request_entity import RequestEntity, RequestCategoryEntity
from google.appengine.ext import db

class RequestManager:
    """ Requests management for both requestor and responder """
    @classmethod
    def list_categories(cls):
        """ Return the list of request categories """
        return RequestCategoryEntity.all().fetch(100)

class RequestorRequestManager:
    """ Create, update, delete, list and manage requests for a requestor """
    
    def __init__(self, requestor_key):
        self._requestor_key = requestor_key

    def create_request(self, category_id, subject, notes):
        ''' Create a new request '''
        request = RequestEntity.create(requestor = self._requestor_key, category_id = category_id, subject = subject, notes = notes)
        request.put()
        return request

    def list_requests(self):
        """ Retrieve the requests created by the specified user """
        query = db.Query(RequestEntity).filter('requestor', self._requestor_key)
        return query.fetch(limit = 20)
        
class ResponderRequestManager:
    def list_requests(self):
        """ Retrieve the list of requests """
        return RequestEntity.all().fetch(1000);