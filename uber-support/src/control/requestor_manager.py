'''
Created on May 14, 2011

@author: Antonio Bello - Elapsus
'''
from model.requestor_entity import RequestorEntity
from model import DuplicatedEntityException

class RequestorManager:
    def __init__(self, email):
        self._email = email
        self._requestor = RequestorEntity.all().filter('email = ', self._email).get()

    def create_requestor(self, name, phone, company):
        try:
            self._requestor = RequestorEntity.create(email = self._email, name = name, phone = phone, company = company)
            self._requestor.put()
        except(DuplicatedEntityException):
            raise RequestorException()
    
    def is_new(self):
        return self._requestor == None
    
    def get_requestor(self):
        return self._requestor
    
class RequestorException(Exception):
    """ Exception to deal with requestor errors """
    pass