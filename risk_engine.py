import random

class RiskEngine:

  def run(self):
    random_number = random.randint(1, 100) 
    if random_number >= 50:
      return False 
    else:
      return True 
