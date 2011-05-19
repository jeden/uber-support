'''
Created on May 14, 2011

@author: Antonio Bello - Elapsus
'''
from model.request_entity import RequestEntity
from google.appengine.ext import db

class RequestManager:
    """ Create, update, delete and list requests """
    
    def __init__(self, requestor_key):
        self._requestor_key = requestor_key

    def create_request(self, category, subject, notes):
        ''' Create a new request '''
        request = RequestEntity.create(requestor = self._requestor_key, category = category, subject = subject, notes = notes)
        request.put()
        return request

    def list_requests(self):
        """ Retrieve the requests created by the specified user """
        query = db.Query(RequestEntity).filter('requestor', self._requestor_key)
        return query.fetch(limit = 20)
        
        