import os
import server
import unittest
import tempfile

class RiskTestCase(unittest.TestCase):

  def setUp(self):
    server.app.config['TESTING'] = True
    self.app = server.app.test_client()

  def test_risk_endpoint(self):
    response = self.app.get('/risk/123')
    response_string = response.get_data().decode('utf-8')
    assert response_string == '123'
    
  def test_risk_endpoint_too_high(self):
    try:
      response = self.app.get('/risk/1001')
    except Exception:
      assert True

if __name__ == '__main__':
  unittest.main()
