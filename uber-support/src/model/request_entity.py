'''
Created on May 17, 2011

@author: Antonio Bello - Elapsus
'''
from model import DbModel
from google.appengine.ext import db

class RequestEntity(DbModel):
    requestor = db.ReferenceProperty(required = True)
    category = db.StringProperty(required = True)
    subject = db.StringProperty(required = True)
    notes = db.TextProperty(required = True)
    submitted_on = db.DateTimeProperty(auto_now = True)
    
    @classmethod
    def create(cls, requestor, category, subject, notes):
        return cls(requestor = requestor, category = category, subject = subject, notes = notes)
        
