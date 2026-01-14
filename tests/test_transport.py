import unittest
from unittest.mock import MagicMock, patch
from onebullex.transport.http import HTTPClient
from onebullex.config import TEST_CONFIG
from onebullex.errors import ServerError, ClientError

class TestHTTPClient(unittest.TestCase):
    def setUp(self):
        self.client = HTTPClient(TEST_CONFIG)
        self.client.rate_limiter = MagicMock() # Disable rate limiting delay

    @patch("requests.Session.request")
    def test_request_success(self, mock_req):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"code": 0, "msg": "success", "data": {"id": 1}}
        mock_req.return_value = mock_resp
        
        data = self.client.get("/test")
        self.assertEqual(data["id"], 1)

    @patch("requests.Session.request")
    def test_server_error_retry(self, mock_req):
        # Fail twice with 500, then succeed
        bad_resp = MagicMock()
        bad_resp.status_code = 500
        
        good_resp = MagicMock()
        good_resp.status_code = 200
        good_resp.json.return_value = {"code": 0, "data": "ok"}
        
        mock_req.side_effect = [bad_resp, bad_resp, good_resp]
        
        data = self.client.get("/retry")
        self.assertEqual(data, "ok")
        self.assertEqual(mock_req.call_count, 3)

    @patch("requests.Session.request")
    def test_client_error_no_retry(self, mock_req):
        bad_resp = MagicMock()
        bad_resp.status_code = 400
        bad_resp.json.return_value = {"code": 20001, "msg": "Bad Param"}
        mock_req.return_value = bad_resp
        
        with self.assertRaises(ClientError):
            self.client.get("/bad")
            
        self.assertEqual(mock_req.call_count, 1)

if __name__ == '__main__':
    unittest.main()
