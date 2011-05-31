'''
Created on May 13, 2011

@author: Antonio Bello - Elapsus
'''
from control.request_manager import RequestManager
from model.request_entity import RequestEntity
from test.test_manage_requestor import Test_ManageRequestor
from test.test_base_appengine_datastore_tester import BaseAppengineDatastoreTester
from test import helpers

class Test_ManageRequest(BaseAppengineDatastoreTester):
    """
        Request creation and update verification
    """
    
    def setUp(self):
        BaseAppengineDatastoreTester.setUp(self)
        
        self.requestor_manager = Test_ManageRequestor()._create_dummy_requestor(1)
        self.request_manager = RequestManager(self.requestor_manager.get_requestor())
    
        helpers.create_dummy_request_categories()
    
    def test_add_new_request(self):
        request = helpers.create_dummy_request(self.request_manager, 1)
        self.verify_entity_instance(request, RequestEntity)
           
    def test_list_requests(self):
        """ Add 3 requests and verify that the method returning the list of requests work as expected """
        requests = self.request_manager.list_requests()
        self.assertEqual(len(requests), 0)
        
        helpers.create_dummy_request(self.request_manager, 1)
        helpers.create_dummy_request(self.request_manager, 2)
        helpers.create_dummy_request(self.request_manager, 3)

        requests = self.request_manager.list_requests()
        self.assertEqual(len(requests), 3)
