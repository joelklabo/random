#!/usr/bin/env python3

from flask import Flask, Response 
from flask import request
from risk_engine import RiskEngine
from invalid_usage import InvalidUsage

# Import from the 21 Bitcoin Develper Library
from two1.lib.wallet import Wallet
from two1.lib.bitserv.flask import Payment
from two1.commands.config import Config

from two1.lib.util import zerotier 

PORT = 5001
MAX_RISK_AMOUNT = 1000
MIN_RISK_AMOUNT = 10

# Configure the app
app = Flask(__name__)
wallet = Wallet()
payment = Payment(app, wallet)

@app.route('/risk/<int:risk_amount>')
def risk(risk_amount):

  transfer = bitcoin_transfer_dict(request)
  if transfer:
    # The user has made the payment request
    print(transfer)
  else:
    # Return a 402 so user can request with payment
    return payment_required_response(risk_amount)

  if risk_amount > MAX_RISK_AMOUNT:
    error_string = 'Risk amount must be less than {:d}'.format(MAX_RISK_AMOUNT)
    raise InvalidUsage(error_string, status_code=400)

  if risk_amount < MIN_RISK_AMOUNT:
    error_string = 'Risk amount must be more than {:d}'.format(MIN_RISK_AMOUNT)
    raise InvalidUsage(error_string, status_code=400)

  if RiskEngine().run():
    # Client won, send bits
    reward_amount = reward(risk_amount)
    send_bittransfer(username, reward_amount)
    return winner_message(username, reward_amount)
  else:
    # Client lost, return message
    return loser_message(username, risk_amount)

def payment_required_response(amount):
  resp = Response('Payment Required')
  resp.status_code = 402
  resp.headers['Bitcoin-Micropayment-Server'] = payment_server_address() 
  resp.headers['Username'] = Config().username
  resp.headers['Price'] = amount
  resp.headers['Bitcoin-Address'] = wallet.get_payout_address() 
  print(resp.headers)
  return resp

def payment_server_address():
  return 'http://{0}:{0}/payment'.format(zerotier.device_ip(), PORT) 

def bitcoin_transfer_dict(request):
  transfer = request.headers.get('Bitcoin-Transfer')

def winner_message(user, reward):
  return 'Congratulations {0} you won {0} satoshis!'.format(user, reward)

def loser_message(user, risk):
  return 'Sorry {0}, you lost {0}. Try again!'.format(user, risk)

def reward(risk):
  return risk * 2

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
  response = jsonify(error.to_dict())
  response.status_code = error.status_code
  return response

if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0', port=PORT)
