from flask import render_template, Flask, request, redirect, flash
from app import app
import requests
from twilio.rest import TwilioRestClient
import twilio.twiml
import os


leagueAPI = os.environ['LEAGUE_API']

@app.route("/", methods=['GET', 'POST'])
def main():
    toGet = request.values.get('Body', None)

    message = str(composeMessage(toGet))

    resp = twilio.twiml.Response()
    resp.message(message)
 
    return str(resp)

def composeMessage(summonerName):
    summonerNameURL = "https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/"+summonerName + "/"

    query = {
                "api_key": leagueAPI
              }
    response = requests.get(summonerNameURL, params = query)
    idData = response.json()

    id = idData[summonerName.lower()]["id"]

    gameURL = "https://na.api.pvp.net/observer-mode/rest/consumer/getSpectatorGameInfo/NA1/" + id + "/"

    response = requests.get(gameURL, params = query)
    gameData = response.json()

    participantList = gameData["participants"]
    infoList = []
    for x in participantList:
        infoList.append([x["summonerName"],x["teamId"], x["summonerId"]])
        if x["summonerId"] == id:
            team = x["teamId"]
    opposingTeam =  []
    for x in infoList:
        if x[1] != team:
            opposingTeam.append([x[0],x[2]])

    finList = []

    for x in opposingTeam:
        leagueURL = "https://na.api.pvp.net/api/lol/na/v2.5/league/by-summoner/" + x[1] + "/"
        response = requests.get(leagueURL, params = query)
        leagueData = response.json()
        finList.append(x[0] + "-" + leagueData[x[1]]["tier"])

    ret = ""
    for x in finList:
        ret += (x + "\n")
    return ret
