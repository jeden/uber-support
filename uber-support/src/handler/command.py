'''
Created on May 19, 2011

@author: Antonio Bello - Elapsus
'''
from utils import doRender
import simplejson

class CommandBase:
    """ Base class for async commands """
    
    __valid = False

    def __init__(self, handler, parameters):
        self.__handler = handler
        self.__parameters = parameters

    def validate(self):
        """ Input validation """
        self.__valid = True
    
    def _execute(self):
        """ Overrideable method executing the command """
        pass
    
    @property
    def valid(self):
        return self.__valid
    
    @property
    def parameters(self):
        return self.__parameters
    
    def execute(self):
        """
            Command execution
            Actual execution is delegated to the overrideable _execute method
        """
        try:
            self.validate()
        except:
            raise
        return self._execute()

    def render_template(self, template, parameters):
        """ Render from template """
        return doRender(self.__handler, template, parameters)
    
    def render_content(self, content):
        self.__handler.response.out.write(content)
    
    def jsonize(self, model):
        return unicode(simplejson.dumps(model.to_dict()))
        
