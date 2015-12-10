#!/usr/bin/env python3

from flask import Flask, Response, request
from flask.ext.responses import json_response
from risk_engine import RiskEngine
from objectifier import Objectifier
from two1.lib.wallet import Wallet
from two1.lib.bitserv.flask import Payment
from two1tools.two1tools.bittransfer import *
from cfgtodict import ConfigToDictionary


PORT = 5001
DEFAULT_RISK_AMOUNT = 100

# Configure the app
app = Flask(__name__)
wallet = Wallet()
payment = Payment(app, wallet)

# Read in server info
about = ConfigToDictionary('info.cfg').dict() 

@app.route('/')
@app.route('/info')
def info():
  return json_response(about)

@app.route('/risk')
@payment.required(DEFAULT_RISK_AMOUNT)
def risk():
  if RiskEngine().run():
    reward_amount = reward(DEFAULT_RISK_AMOUNT)
    transfer_dictionary = bitcoin_transfer_dict(request)
    payee_username = transfer_dictionary['payer']
    send_bittransfer(payee_username, reward_amount)
    return winner_message(payee_username, reward_amount)
  else:
    return loser_message(DEFAULT_RISK_AMOUNT)

def bitcoin_transfer_dict(request):
  return Objectifier(request.headers.get('Bitcoin-Transfer'))

def winner_message(user, reward):
  return 'Congratulations {0} you won {1} satoshis!'.format(user, reward)

def loser_message(risk):
  return 'Sorry, you lost {0} satoshis. Try again!'.format(risk)

def reward(risk):
  return risk * 2

if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0', port=PORT)
