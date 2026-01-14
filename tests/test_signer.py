import unittest
from unittest.mock import MagicMock
from onebullex.auth.signer import Signer
from onebullex.utils import TimeSync

class TestSigner(unittest.TestCase):
    def setUp(self):
        self.mock_time = MagicMock(spec=TimeSync)
        self.mock_time.get_timestamp_str.return_value = "1700000000000"
        self.signer = Signer("my_key", "my_secret", "my_id", self.mock_time)

    def test_sign_parameters(self):
        params = {
            "symbol": "BTCUSDT",
            "side": 1,
            "verbose": True
        }
        headers = self.signer.sign(params)
        
        self.assertEqual(headers["X-API-Key"], "my_key")
        self.assertEqual(headers["X-Identify"], "my_id")
        self.assertEqual(headers["X-Timestamp"], "1700000000000")
        self.assertTrue("X-Signature" in headers)
        self.assertTrue("X-Nonce" in headers)
        
        # Verify Signature Construction Manual Check?
        # Content = timestamp + nonce + sorted_query
        # sorted_query = side=1&symbol=BTCUSDT&verbose=true
        # We implicitly test that it doesn't crash and returns required headers.
        
    def test_sign_empty_params(self):
        headers = self.signer.sign({})
        self.assertTrue("X-Signature" in headers)

if __name__ == '__main__':
    unittest.main()
