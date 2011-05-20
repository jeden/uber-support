import gaesessions

class Session(gaesessions.Session):
    def is_logged_in(self):
        return self.has_key('user_email')
    
    def register_login(self, email):
        self['user_email'] = email
        
    def get_requestor(self):
        return self.get('requestor', None)
    
    def set_requestor(self, requestor):
        self['requestor'] = requestor
