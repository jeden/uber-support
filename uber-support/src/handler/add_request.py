'''
Created on May 20, 2011

@author: Antonio Bello - Elapsus
'''
from google.appengine.ext import webapp
from control.requestor_manager import RequestorManager
from control.request_manager import RequestManager
from handler import Session
from django import forms
from utils import doRender

class RequestForm(forms.Form):
    email = forms.EmailField(label='Email address')
    category = forms.ChoiceField(label='Category')
    subject = forms.CharField(label='Subject')
    notes = forms.CharField(label='Notes', widget = forms.Textarea)
    name = forms.CharField(label='Your Name')
    phone = forms.CharField(label='Your Phone')
    company = forms.CharField(label='Your Company')
    
    email.widget.attrs = {'onblur': 'changeRequestor(this)'} # display the list of current requests
    
    list = [(str(entity.key().id()), entity.category) for entity in RequestManager.list_categories()]
    list.insert(0, ('', '--Select--'))
    category.choices = list
    
class AddRequestHandler(webapp.RequestHandler):
    """ Form to add a new request """

    def __init__(self):
        self.__session = Session()

    def get(self, form = RequestForm()):
        doRender(self, 'add_request.html', {
                                            'form': form,
                                            'requestor': self.__session.get_requestor(),
                                            'is_logged_in': self.__session.is_logged_in()})
        
    def post(self):
        form = RequestForm(data = self.request.POST)

        if form.is_valid():
            email = self.request.get('email')
            category = int(self.request.get('category'))
            subject = self.request.get('subject')
            notes = self.request.get('notes')
    
            requestor_manager = RequestorManager(email)
            
            if (self.__session.is_logged_in() == False):
                name = self.request.get('name')
                phone = self.request.get('phone')
                company = self.request.get('company')
                
                if requestor_manager.is_new():
                    requestor_manager.create_requestor(name, phone, company)
                self.__session.register_login(email)
                self.__session.set_requestor(requestor_manager.get_requestor())
            
            request_manager = RequestManager(requestor_manager.get_requestor())
            request_manager.create_request(category, subject, notes)

        self.get(form = form)

