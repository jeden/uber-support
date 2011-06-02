'''
Created on May 14, 2011

@author: Antonio Bello - Elapsus
'''
from model.request_entity import RequestEntity, RequestCategoryEntity
from google.appengine.ext import db
from utils.enum import Enum

RequestSortOrder = Enum( [ 'REQUESTOR', 'RANK', 'CATEGORY', 'SUBMITTED_ON' ] )

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
    def list_requests(self, status, sort_by = None, sort_descending = None):
        """ 
            Retrieve the list of requests
            
            PARAMETERS:
            * status: filter requests by status 
        """

        query = RequestEntity.all().filter('status =', status)
        sign = sort_descending and '-' or ''
        
        if sort_descending is None:
            sort_descending = False
        
        if sort_by == RequestSortOrder.REQUESTOR:
            requests = query.order('%srequestor' % sign).fetch(1000)
        elif sort_by == RequestSortOrder.RANK:
            requests = query.fetch(1000)
            requests.sort(key = lambda request: request.requestor.rank, reverse = sort_descending)
        elif sort_by == RequestSortOrder.CATEGORY:
            requests = query.fetch(1000)
            requests.sort(key = lambda request: request.category.category, reverse = sort_descending)
        elif sort_by == RequestSortOrder.SUBMITTED_ON:
            requests = query.order('%ssubmitted_on' % sign).fetch(1000)
        else:
            requests = query.fetch(1000)
        
        return requests
