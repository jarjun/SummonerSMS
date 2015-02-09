from flask import render_template, Flask, request, redirect, flash
from app import app
import requests
from twilio.rest import TwilioRestClient
from config import *
import twilio.twiml

client = TwilioRestClient(config.account_sid, config.auth_token)


@app.route("/", methods=['GET', 'POST'])
def main():
    toGet = request.values.get('Body', None)

    message = composeMessage(toGet)

    resp = twilio.twiml.Response()
    resp.message(message)
 
    return str(resp)

def composeMessage(summonerName):
    gameURL = "https://na.api.pvp.net/observer-mode/rest/consumer/getSpectatorGameInfo/NA1/"
    leagueURL = "https://na.api.pvp.net/api/lol/na/v2.5/league/by-summoner/"
    summonerNameURL = "https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/"+summonerName

    idQuery = {
                "api_key": config.leagueAPI
              }
    response = requests.get(summonerNameURL, params = idQuery)
    idData = response.json()

    return idData[summonerName]["id"]
