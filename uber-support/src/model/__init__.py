from google.appengine.ext import db

#
# Model utilities
#

class  DbModel(db.Model):
    def to_dict(self):
        return dict([(p, unicode(getattr(self, p))) for p in self.properties()])        

    @classmethod
    def check_for_uniqueness(cls, field_name, field_value):
        """
        Verify uniqueness of the specified pair (field, value)
    
        Parameters:
        - field_name: name of the field
        - field_value: the field value to be checked for uniqueness
    
        Throw a DuplicatedEntityException if the specified value
        is already used
        """
    
        query = cls.all(keys_only = True).filter(field_name, field_value)
        entity = query.get()
        if entity:
            raise DuplicatedEntityException(cls, field_name, field_value)

#
# Exceptions
#
    
class DuplicatedEntityException(Exception):
    """  Thrown when a field uniqueness constraint is violated """
    def __init__(self, model, field_name, field_value):
        Exception.__init__(self, "Uniqueness constraint violated: model = %s, field name = %s, field value = %s" % (model, field_name, field_value))
