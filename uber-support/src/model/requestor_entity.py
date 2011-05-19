'''
Created on May 14, 2011

@author: Antonio Bello - Elapsus
'''
from google.appengine.ext import db
from model import DbModel

class RequestorEntity(DbModel):
    email = db.EmailProperty(required = True)
    name = db.StringProperty(required = True)
    phone = db.PhoneNumberProperty(required = True)
    company = db.StringProperty(required = True)
    
    @classmethod
    def create(cls, email, name, phone, company):
        RequestorEntity.check_for_uniqueness("email", email)
        return cls(email = email, name = name, phone = phone, company = company)