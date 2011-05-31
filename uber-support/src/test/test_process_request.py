'''
Created on May 27, 2011

@author: Antonio Bello - Elapsus
'''
from test.test_base_appengine_datastore_tester import BaseAppengineDatastoreTester
from test.helpers import create_dummy_request_categories, create_dummy_request
from test.test_manage_requestor import Test_ManageRequestor
from control.request_manager import RequestManager
from test import helpers

class Test_ProcessRequest(BaseAppengineDatastoreTester):
    """ Request processing """
    
    def setUp(self):
        BaseAppengineDatastoreTester.setUp(self)
        
        self.requestor_manager = Test_ManageRequestor()._create_dummy_requestor(1)
        self.request_manager = RequestManager(self.requestor_manager.get_requestor())
        
        create_dummy_request_categories()

    def test_retrieve_open_requests(self):
        """ Add some requests and retrieve them, verifying they match """
        helpers.create_dummy_request(self.request_manager, 1, 5)
        
        requests = self.request_manager.list_requests()
        
        self.assertEqual(len(requests), 5)
        
    def test_retrieve_open_requests_by_requestor(self):
        requestor_manager_1 = self.requestor_manager
        request_manager_1 = self.request_manager
        
        requestor_manager_2 = Test_ManageRequestor()._create_dummy_requestor(2)
        request_manager_2 = RequestManager(requestor_manager_2.get_requestor())
        
        # Create 7 requests, mixing the 2 requestors
        create_dummy_request(request_manager_1, 1) 
        create_dummy_request(request_manager_2, 2) 
        create_dummy_request(request_manager_1, 3) 
        create_dummy_request(request_manager_2, 4) 
        create_dummy_request(request_manager_1, 5) 
        create_dummy_request(request_manager_2, 6) 
        create_dummy_request(request_manager_1, 7)
        
        requests_1 = request_manager_1.list_requests()
        requests_2 = request_manager_2.list_requests()
        
        # Verify that each request manager returns own requests only
        self.assertEqual(len(requests_1), 4)
        self.assertEqual(len(requests_2), 3)
         
        for request in requests_1:
            self.assertEqual(request.requestor.key(), requestor_manager_1.get_requestor().key())
             
        for request in requests_2:
            self.assertEqual(request.requestor.key(), requestor_manager_2.get_requestor().key())
