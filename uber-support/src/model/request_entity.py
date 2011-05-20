'''
Created on May 17, 2011

@author: Antonio Bello - Elapsus
'''
from model import DbModel
from google.appengine.ext import db

class RequestCategoryEntity(DbModel):
    category = db.StringProperty(required = True)
    
    def __repr__(self):
        return self.category

class RequestEntity(DbModel):
    requestor = db.ReferenceProperty(required = True)
    category = db.ReferenceProperty(reference_class = RequestCategoryEntity, required = True)
    subject = db.StringProperty(required = True)
    notes = db.TextProperty(required = True)
    submitted_on = db.DateTimeProperty(auto_now = True)
    
    @classmethod
    def create(cls, requestor, category_id, subject, notes):
        key = db.Key.from_path('RequestCategoryEntity', category_id)
        return cls(requestor = requestor, category = key, subject = subject, notes = notes)
