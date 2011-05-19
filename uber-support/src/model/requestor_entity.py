'''
Created on May 14, 2011

@author: Antonio Bello - Elapsus
'''
from google.appengine.ext import db
from model.model_utils import check_for_uniqueness

class RequestorEntity(db.Model):
    email = db.EmailProperty(required = True)
    name = db.StringProperty(required = True)
    phone = db.PhoneNumberProperty(required = True)
    company = db.StringProperty(required = True)
    
    @classmethod
    def create(cls, email, name, phone, company):
        check_for_uniqueness(RequestorEntity, "email", email)
        return cls(email = email, name = name, phone = phone, company = company)