#!/usr/bin/env python3

from flask import Flask
from flask import request

# Import from the 21 Bitcoin Develper Library
#from two1.lib.wallet import Wallet
#from two1.lib.bitserv.flask import Payment

PORT = 5000

# Configure the app
app = Flask(__name__)
#wallet = Wallet()
#payment = Payment(app, wallet)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=PORT)
