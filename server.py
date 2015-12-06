#!/usr/bin/env python3

from flask import Flask, jsonify
from flask import request

from invalid_usage import InvalidUsage

# Import from the 21 Bitcoin Develper Library
#from two1.lib.wallet import Wallet
#from two1.lib.bitserv.flask import Payment

PORT = 5000
MAX_RISK_AMOUNT = 10000

# Configure the app
app = Flask(__name__)
#wallet = Wallet()
#payment = Payment(app, wallet)

@app.route('/risk/<int:risk_amount>')
def risk(risk_amount):

  if risk_amount > MAX_RISK_AMOUNT:
    error_string = 'Risk amount must be less than {:d}'.format(MAX_RISK_AMOUNT)
    raise InvalidUsage(error_string, status_code=400)

  return '{:d}'.format(risk_amount)

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
  response = jsonify(error.to_dict())
  response.status_code = error.status_code
  return response

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=PORT)
