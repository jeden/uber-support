'''
Created on May 27, 2011

@author: Antonio Bello - Elapsus
'''
from model.request_entity import RequestCategoryEntity

def get_request_category():
    """ Return the first request category in the datastore """
    return RequestCategoryEntity.all().get()

def create_dummy_request_categories():
    """ Create dummies request categories """
    category = RequestCategoryEntity(category = 'hardware')
    category.put()

    category = RequestCategoryEntity(category = 'software')
    category.put()

def create_dummy_request(request_manager, index, count = 1):
    """ Create one or more dummy requests """
    category = get_request_category()
    
    if count == 1:
        return request_manager.create_request(
            category_id = category.key().id(),
            subject = 'request_%i' % index,
            notes = 'this is a sample request %i' % index,
        )
    else:
        for i in range(index, index + count):
            request_manager.create_request(
                                           category_id = category.key().id(),
                                           subject = 'request_%i' %i,
                                           notes = 'this is a sample request %i' % i
                                           )
        
