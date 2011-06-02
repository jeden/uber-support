'''
Created on May 13, 2011

@author: Antonio Bello - Elapsus
'''
from control.request_manager import RequestManager, RequestorRequestManager,\
    ResponderRequestManager, RequestSortOrder
from model.request_entity import RequestEntity, RequestCategoryEntity,\
    RequestStatus
from test.test_base_appengine_datastore_tester import BaseAppengineDatastoreTester
from test import helpers
from google.appengine.ext import db
import datetime

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
        """ Verify that a new request has the "UNASSIGNED" status """
        request = helpers.create_dummy_request(self.request_manager, 1)
        self.assertEquals(request.status, RequestStatus.UNASSIGNED)

class Test_ManageResponderRequests(BaseAppengineDatastoreTester):
    """
        Request management tests for responders 
    """
    def setUp(self):
        super(Test_ManageResponderRequests, self).setUp()
        
        (self._category_1, self._category_2) = helpers.create_dummy_request_categories()

        # Create 2 requestors
        self._requestor_manager_1 = helpers.create_dummy_requestor(1)
        request_manager_1 = RequestorRequestManager(self._requestor_manager_1.get_requestor())
        
        self._requestor_manager_2 = helpers.create_dummy_requestor(2)
        request_manager_2 = RequestorRequestManager(self._requestor_manager_2.get_requestor())

        # Create 7 requests, mixing the 2 requestors
        helpers.create_dummy_request(request_manager_1, 1) 
        helpers.create_dummy_request(request_manager_2, 2) 
        helpers.create_dummy_request(request_manager_1, 3) 
        helpers.create_dummy_request(request_manager_2, 4) 
        helpers.create_dummy_request(request_manager_1, 5) 
        helpers.create_dummy_request(request_manager_2, 6) 
        helpers.create_dummy_request(request_manager_1, 7)
        
        self._request_manager = ResponderRequestManager()
        
    def test_retrieve_unassigned_requests(self):
        """ Verify that all open requests are correctly retrieved """
        requests = self._request_manager.list_requests(RequestStatus.UNASSIGNED)
        
        self.assertEqual(len(requests), 7)
        
        for request in requests:
            self.verify_entity_instance(request, RequestEntity)
            self.assertEquals(request.status, RequestStatus.UNASSIGNED)
            
        # Verify that there is no OPEN or CLOSED request
        requests = self._request_manager.list_requests(RequestStatus.OPEN)
        self.assertEqual(len(requests), 0)

        requests = self._request_manager.list_requests(RequestStatus.CLOSED)
        self.assertEqual(len(requests), 0)
        
    def test_sort_by_requestor(self):
        """ Verify sort by requestor """
        
        requests = self._request_manager.list_requests(RequestStatus.UNASSIGNED)
        self.assertEqual(len(requests), 7)
        requestor_1 = str(requests[0].requestor)
        requestor_2 = str(requests[1].requestor)
        
        requests = self._request_manager.list_requests(RequestStatus.UNASSIGNED, sort_by = 'REQUESTOR')
        self.assertEqual(len(requests), 7)
                
        self.assertIsInstance(requestor_1, str)
        self.assertIsInstance(requestor_2, str)
        
        self.assertLess(requestor_1, requestor_2)
        
        self.assertEqual(str(requests[0].requestor), requestor_1)
        self.assertEqual(str(requests[1].requestor), requestor_1)
        self.assertEqual(str(requests[2].requestor), requestor_1)
        self.assertEqual(str(requests[3].requestor), requestor_1)
        self.assertEqual(str(requests[4].requestor), requestor_2)
        self.assertEqual(str(requests[5].requestor), requestor_2)
        self.assertEqual(str(requests[6].requestor), requestor_2)
        
    def test_sort_by_rank(self):
        ''' Verify sort by rank '''
        
        # Change the requestors rank
        requestor_1 = self._requestor_manager_1.get_requestor()
        requestor_1.rank = 20
        requestor_1.put()
        
        requestor_2 = self._requestor_manager_2.get_requestor()
        requestor_2.rank = 10
        requestor_2.put()
    
        # Retrieve requests
        requests = self._request_manager.list_requests(RequestStatus.UNASSIGNED, sort_by = 'RANK')
        self.assertEqual(len(requests), 7)

        # Verify that requestor 2's requests come first
        self.assertEqual(requests[0].requestor.key(), requestor_2.key())
        self.assertEqual(requests[1].requestor.key(), requestor_2.key())
        self.assertEqual(requests[2].requestor.key(), requestor_2.key())
        self.assertEqual(requests[3].requestor.key(), requestor_1.key())
        self.assertEqual(requests[4].requestor.key(), requestor_1.key())
        self.assertEqual(requests[5].requestor.key(), requestor_1.key())
        self.assertEqual(requests[6].requestor.key(), requestor_1.key())
                
    def test_sort_by_category(self):
        ''' Verify sort by category '''

        # Retrieve requests
        requests = self._request_manager.list_requests(RequestStatus.UNASSIGNED)
        self.assertEqual(len(requests), 7)

        # Reassign request categories
        requests[0].category = self._category_2
        requests[1].category = self._category_2
        requests[2].category = self._category_1
        requests[3].category = self._category_2
        requests[4].category = self._category_1
        requests[5].category = self._category_1
        requests[6].category = self._category_2

        db.put(requests)

        # Reload requests
        requests = self._request_manager.list_requests(RequestStatus.UNASSIGNED, sort_by = 'CATEGORY')

        # Verify that requests are sorted by category_1 first, then category_2
        self.assertEqual(requests[0].category.key(), self._category_1.key())
        self.assertEqual(requests[1].category.key(), self._category_1.key())
        self.assertEqual(requests[2].category.key(), self._category_1.key())
        self.assertEqual(requests[3].category.key(), self._category_2.key())
        self.assertEqual(requests[4].category.key(), self._category_2.key())
        self.assertEqual(requests[5].category.key(), self._category_2.key())
        self.assertEqual(requests[6].category.key(), self._category_2.key())
    
    def test_sort_by_submitted_on(self):
        ''' Verify sort by submission date '''

        # Retrieve requests
        requests = self._request_manager.list_requests(RequestStatus.UNASSIGNED)
        self.assertEqual(len(requests), 7)
        
        # Reassign request dates
        requests[0].submitted_on = datetime.datetime.strptime('2011-06-15', '%Y-%m-%d')
        requests[1].submitted_on = datetime.datetime.strptime('2011-05-16', '%Y-%m-%d')
        requests[2].submitted_on = datetime.datetime.strptime('2011-07-15', '%Y-%m-%d')
        requests[3].submitted_on = datetime.datetime.strptime('2011-06-20', '%Y-%m-%d')
        requests[4].submitted_on = datetime.datetime.strptime('2011-04-15', '%Y-%m-%d')
        requests[5].submitted_on = datetime.datetime.strptime('2011-05-15', '%Y-%m-%d')
        requests[6].submitted_on = datetime.datetime.strptime('2012-06-15', '%Y-%m-%d')
        
        db.put(requests)

        # Reload requests
        requests = self._request_manager.list_requests(RequestStatus.UNASSIGNED, sort_by = RequestSortOrder.SUBMITTED_ON)
        
        # Verify that requests are sorted by date
        self.assertLess(requests[0].submitted_on, requests[1].submitted_on) 
        self.assertLess(requests[1].submitted_on, requests[2].submitted_on) 
        self.assertLess(requests[2].submitted_on, requests[3].submitted_on) 
        self.assertLess(requests[3].submitted_on, requests[4].submitted_on) 
        self.assertLess(requests[4].submitted_on, requests[5].submitted_on) 
        self.assertLess(requests[5].submitted_on, requests[6].submitted_on) 
        

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