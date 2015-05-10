from flask import render_template, Flask, request, redirect, flash
from app import app
import requests
from twilio.rest import TwilioRestClient
import twilio.twiml
import os
import time

leagueAPI = os.environ['LEAGUE_API']

@app.route("/", methods=['GET', 'POST'])
def main():
    try:
        toGet = request.values.get('Body', None)

        message = str(composeMessage(toGet))

        resp = twilio.twiml.Response()
        resp.message(message)
    except:
        return "Internal Service Error"
 
    return str(resp)

def composeMessage(summonerName):
    summonerNameURL = "https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/"+ summonerName + "/"

    query = {
                "api_key": leagueAPI
              }
    try:
        response = requests.get(summonerNameURL, params = query)
        idData = response.json()
        name = summonerName.split(" ")
        name = "".join(name)
        id = idData[name.lower()]["id"]
    except:
        return "Summoner not found"


    try:
        gameURL = "https://na.api.pvp.net/observer-mode/rest/consumer/getSpectatorGameInfo/NA1/" + str(id) + "/"

        response2 = requests.get(gameURL, params = query)
        gameData = response2.json()
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
    except:
        return "Not in game"

    try:
        d = {}
        for x in opposingTeam:
            d[str(x[1])] = x[0]
        finList = []
    except:
        return "Error Code 1"
    try:
        leagueURL = "https://na.api.pvp.net/api/lol/na/v2.5/league/by-summoner/" + str(opposingTeam[0][1]) + "," + str(opposingTeam[1][1]) + "," + str(opposingTeam[2][1]) + "," + str(opposingTeam[3][1]) + "," + str(opposingTeam[4][1]) + "/" + "entry" + "/"
        response3 = requests.get(leagueURL, params = query)
        leagueData = response3.json()
    except:
        return "Request Error"

    try:
        for x in d:
            try:
                finList.append(str(d[x]) + "-" + str(leagueData[x][0]["tier"]) + " " + str(leagueData[x][0]["entries"][0]["division"]))
            except:
                finList.append(str(d[x]) + "-" + "UNRANKED")
        ret = ""
        for x in finList:
            ret += x
            ret += "\n"
    except:
        return "Error Code 2"

    try:
        recordingURL = "http://na.op.gg/summoner/ajax/requestRecording.json/gameId=" + str(id) + "/"
        response4 = requests.get(recordingURL, params = null)
        record = response.json()
        ret += record
        if response["success"] == "true":
            ret += "Recording Successful"
    except:
        ret += "Recording Failure"

    return ret