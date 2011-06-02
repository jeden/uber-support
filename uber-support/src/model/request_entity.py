'''
Created on May 17, 2011

@author: Antonio Bello - Elapsus
'''
from model import DbModel
from google.appengine.ext import db
from utils.enum import Enum

RequestStatus = Enum(['NONE', 'UNASSIGNED', 'OPEN', 'CLOSED'])

class RequestCategoryEntity(DbModel):
    """ Request Category """
    category = db.StringProperty(required = True)
    
    def __repr__(self):
        return self.category

class RequestEntity(DbModel):
    """ Request """
    requestor = db.ReferenceProperty(required = True)
    category = db.ReferenceProperty(reference_class = RequestCategoryEntity, required = True)
    subject = db.StringProperty(required = True)
    notes = db.TextProperty(required = True)
    submitted_on = db.DateTimeProperty(auto_now_add = True)
    status = db.StringProperty(required = True, choices = RequestStatus, default = RequestStatus.UNASSIGNED)
    
    @classmethod
    def create(cls, requestor, category_id, subject, notes):
        key = db.Key.from_path('RequestCategoryEntity', category_id)
        return cls(requestor = requestor, category = key, subject = subject, notes = notes)
