'''
Created on May 13, 2011

@author: Antonio Bello - Elapsus
'''
from control.request_manager import RequestManager, RequestorRequestManager,\
    ResponderRequestManager
from model.request_entity import RequestEntity, RequestCategoryEntity,\
    RequestStatus
from test.test_base_appengine_datastore_tester import BaseAppengineDatastoreTester
from test import helpers

class Test_ManageRequestorRequests(BaseAppengineDatastoreTester):
    """
        Request management tests for requestors 
    """
    def setUp(self):
        super(Test_ManageRequestorRequests, self).setUp()
        self.requestor_manager = helpers.create_dummy_requestor(1)
        self.request_manager = RequestorRequestManager(self.requestor_manager.get_requestor())
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

    def test_retrieve_open_requests(self):
        """ Add some requests and retrieve them, verifying they match """
        helpers.create_dummy_request(self.request_manager, 1, 5)
        
        requests = self.request_manager.list_requests()
        
        self.assertEqual(len(requests), 5)
        
    def test_retrieve_open_requests_by_requestor(self):
        requestor_manager_1 = self.requestor_manager
        request_manager_1 = self.request_manager
        
        requestor_manager_2 = helpers.create_dummy_requestor(2)
        request_manager_2 = RequestorRequestManager(requestor_manager_2.get_requestor())
        
        # Create 7 requests, mixing the 2 requestors
        helpers.create_dummy_request(request_manager_1, 1) 
        helpers.create_dummy_request(request_manager_2, 2) 
        helpers.create_dummy_request(request_manager_1, 3) 
        helpers.create_dummy_request(request_manager_2, 4) 
        helpers.create_dummy_request(request_manager_1, 5) 
        helpers.create_dummy_request(request_manager_2, 6) 
        helpers.create_dummy_request(request_manager_1, 7)
        
        requests_1 = request_manager_1.list_requests()
        requests_2 = request_manager_2.list_requests()
        
        # Verify that each request manager returns own requests only
        self.assertEqual(len(requests_1), 4)
        self.assertEqual(len(requests_2), 3)
         
        for request in requests_1:
            self.assertEqual(request.requestor.key(), requestor_manager_1.get_requestor().key())
             
        for request in requests_2:
            self.assertEqual(request.requestor.key(), requestor_manager_2.get_requestor().key())
            
    def test_verify_new_request_status(self):
        """ Verify that a new request has a "open" status """
        request = helpers.create_dummy_request(self.request_manager, 1)
        self.assertEquals(request.status, RequestStatus.OPEN)

class Test_ManageResponderRequests(BaseAppengineDatastoreTester):
    """
        Request management tests for responders 
    """
    def setUp(self):
        super(Test_ManageResponderRequests, self).setUp()
        helpers.create_dummy_request_categories()

        # Create 2 requestors
        requestor_manager_1 = helpers.create_dummy_requestor(1)
        request_manager_1 = RequestorRequestManager(requestor_manager_1.get_requestor())
        
        requestor_manager_2 = helpers.create_dummy_requestor(2)
        request_manager_2 = RequestorRequestManager(requestor_manager_2.get_requestor())

        # Create 7 requests, mixing the 2 requestors
        helpers.create_dummy_request(request_manager_1, 1) 
        helpers.create_dummy_request(request_manager_2, 2) 
        helpers.create_dummy_request(request_manager_1, 3) 
        helpers.create_dummy_request(request_manager_2, 4) 
        helpers.create_dummy_request(request_manager_1, 5) 
        helpers.create_dummy_request(request_manager_2, 6) 
        helpers.create_dummy_request(request_manager_1, 7)
        
        self._request_manager = ResponderRequestManager()
        
    def test_retrieve_open_requests(self):
        """ Verify that all open requests are correctly retrieved """
        requests = self._request_manager.list_requests()
        
        self.assertEqual(len(requests), 7)
        
        for request in requests:
            self.verify_entity_instance(request, RequestEntity)
    

class Test_ManageRequests(BaseAppengineDatastoreTester):
    """ Global request management tests """
    def setUp(self):
        super(Test_ManageRequests, self).setUp()
        self.requestor_manager = helpers.create_dummy_requestor(1)
        self.request_manager = RequestorRequestManager(self.requestor_manager.get_requestor())
        helpers.create_dummy_request_categories()
    
    def test_list_categories(self):
        """ Verify that request categories are correctly retrieved """
        categories = RequestManager.list_categories()
        self.assertGreater(len(categories), 0)
        
        for category in categories:
            self.verify_entity_instance(category, RequestCategoryEntity) 