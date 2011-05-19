'''
Created on May 14, 2011

@author: Antonio Bello - Elapsus
'''

from control.requestor_manager import RequestorManager, RequestorException
from model.requestor_entity import RequestorEntity
from test.test_base_appengine_datastore_tester import BaseAppengineDatastoreTester

class Test_ManageRequestor(BaseAppengineDatastoreTester):
    """ Requestor management tests"""
    
    def setUp(self):
        BaseAppengineDatastoreTester.setUp(self)
    
    def test_create_requestor(self):
        """ Create a new requestor and verify it is correctly stored """
        
        requestor_manager = RequestorManager(email = 'requestor@email.com')
        
        # Verify the requestor does not exist yet
        requestor = requestor_manager.get_requestor()
        self.assertIsNone(requestor)
        self.assertTrue(requestor_manager.is_new)
        
        # Create the requestor
        requestor_manager.create_requestor(
                    name = 'First, Last',
                    phone = '555-405-7685',
                    company = 'My Company, Inc'
                )
        
        # Reinstance the requestor manager
        requestor_manager = RequestorManager(email = 'requestor@email.com')
        
        # Retrieve the requestor and verify it exists
        requestor = requestor_manager.get_requestor()
        
        self.verify_entity_instance(requestor, RequestorEntity)
        
    def test_create_duplicated_requestor(self):
        """ Verify that a new requestor with an existing email cannot be created """
        self._create_dummy_requestor(1)
        
        try:
            self._create_dummy_requestor(1)
            self.fail('Created duplicated requestor')
        except(RequestorException):
            pass
        
    def _create_dummy_requestor(self, index):
        requestor_manager = RequestorManager(email = 'requestor_%i@email.com' % index)

        # Create the requestor
        requestor_manager.create_requestor(
                    name = 'First, Last',
                    phone = '555-405-7685',
                    company = 'My Company, Inc'
                )
        
        return requestor_manager