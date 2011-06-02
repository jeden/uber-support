'''
Created on May 27, 2011

@author: Antonio Bello - Elapsus
'''
from model.request_entity import RequestCategoryEntity
from control.requestor_manager import RequestorManager

def get_request_category():
    """ Return the first request category in the datastore """
    return RequestCategoryEntity.all().get()

def create_dummy_request_categories():
    """ Create dummies request categories """
    category_1 = RequestCategoryEntity(category = 'hardware')
    category_1.put()

    category_2 = RequestCategoryEntity(category = 'software')
    category_2.put()
    
    return (category_1, category_2)

def create_dummy_requestor(index):
    requestor_manager = RequestorManager(email = 'requestor_%i@email.com' % index)

    # Create the requestor
    requestor_manager.create_requestor(
                name = 'First%i, Last' % index,
                phone = '555-405-7685',
                company = 'My Company, Inc'
            )
    
    return requestor_manager
    
def create_dummy_request(request_manager, index, count = 1, category = None):
    """ Create one or more dummy requests """
    if category is None:
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
        
