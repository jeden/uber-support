'''
Created on May 13, 2011

@author: Antonio Bello - Elapsus
'''
from control.request_manager import RequestManager
from model.request_entity import RequestEntity
from test.test_manage_requestor import Test_ManageRequestor
from test.test_base_appengine_datastore_tester import BaseAppengineDatastoreTester

class Test_ManageRequest(BaseAppengineDatastoreTester):
    """
        Request creation and update verification
    """
    
    def setUp(self):
        BaseAppengineDatastoreTester.setUp(self)
        
        self.requestor_manager = Test_ManageRequestor()._create_dummy_requestor(1)
        self.request_manager = RequestManager(self.requestor_manager.get_requestor())
    
    def test_add_new_request(self):
        request = self._create_dummy_request(1)
        self.verify_entity_instance(request, RequestEntity)
           
    def test_list_requests(self):
        """ Add 3 requests and verify that the method returning the list of requests work as expected """
        requestor = self.requestor_manager.get_requestor()
        requests = self.request_manager.list_requests(requestor)
        self.assertEqual(len(requests), 0)
        
        self._create_dummy_request(1)
        self._create_dummy_request(2)
        self._create_dummy_request(3)

        requests = self.request_manager.list_requests(requestor)
        self.assertEqual(len(requests), 3)
           
    def _create_dummy_request(self, index):
        return self.request_manager.create_request(
                    category = 'fix',
                    subject = 'request_%i' % index,
                    notes = 'this is a sample request %i' % index,
                )
