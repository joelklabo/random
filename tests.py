import os
import server
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

  def setUp(self):
    server.app.config['TESTING'] = True
    self.app = server.app.test_client()

  def test_risk_endpoint(self):
    response = self.app.get('/risk/123')
    response_string = response.get_data().decode('utf-8')
    assert response_string == '123'

if __name__ == '__main__':
  unittest.main()
