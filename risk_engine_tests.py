from risk_engine import RiskEngine
import unittest

class RiskEngineTestCase(unittest.TestCase):

  def setUp(self):
    self.engine = RiskEngine()

  def test_roll(self):
    assert self.engine.roll()
    
if __name__ == '__main__':
  unittest.main()
