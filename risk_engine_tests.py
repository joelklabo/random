from risk_engine import RiskEngine
import unittest

class RiskEngineTestCase(unittest.TestCase):

  def setUp(self):
    self.engine = RiskEngine()

  def test_roll_is_near_even(self):
    n = 1000000 
    payout_count = 0
    for roll in range(n):
      if self.engine.run():
        payout_count += 1  
    payout_percentage = float(payout_count)/float(n)
    print(payout_percentage)
    assert (payout_percentage > 0.0 and payout_percentage <= 0.49)
    
if __name__ == '__main__':
  unittest.main()
