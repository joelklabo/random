#!/usr/bin/env python3

from flask import Flask, jsonify
from flask import request
from risk_engine import RiskEngine
from invalid_usage import InvalidUsage

# Import from the 21 Bitcoin Develper Library
from two1.lib.wallet import Wallet
from two1.lib.bitserv.flask import Payment
from two1tools.two1tools.bittransfer import *

PORT = 5001
MAX_RISK_AMOUNT = 1000
MIN_RISK_AMOUNT = 10

# Configure the app
app = Flask(__name__)
wallet = Wallet()
payment = Payment(app, wallet)

@app.route('/risk/<int:risk_amount>')
def risk(risk_amount):

  username = request.args.get('username')

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

def winner_message(user, reward):
  return 'Congratulations {0} you won {:d} satoshis!'.format(user, reward)

def loser_mesage(user, risk):
  return 'Sorry {0}, you lost [:d}. Try again!'.format(user, risk)

def reward(risk):
  return risk * 2

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
  response = jsonify(error.to_dict())
  response.status_code = error.status_code
  return response

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=PORT)
