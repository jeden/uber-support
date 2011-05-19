'''
Created on May 19, 2011

@author: Antonio Bello - Elapsus
'''
from utils import doRender
import simplejson
import types

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
        """ Serialize in JSON format an entity or list of entities """
        if isinstance (model, types.ListType):
            m = [p.to_dict() for p in model]
        else:
            m = model.to_dict()
            
        return unicode(simplejson.dumps(m))
    
    def jsonize_jqgrid(self, model):
        """ Serialize a list of entities in JSON format and specific to the jQgrid grid control """
        map = {
               'total': '1',
               'page': '1',
               'records': str(len(model)),
               'rows': [ self.__add_key(p) for p in model]
               }

        return unicode(simplejson.dumps(map))

    def __add_key(self, entity):
        """ Convert an entity to a dictionary containing all properties, plus the string version of the entity key """
        map = entity.to_dict()
        map['id'] = str(entity.key())
        return map