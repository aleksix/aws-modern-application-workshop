from collections import defaultdict
from boto3.dynamodb.conditions import Key
import boto3

dynamodb = boto3.resource("dynamodb")

players = dynamodb.Table("MysfitsPlayers")
owned_monsters = dynamodb.Table("MysfitsMonsters")


def playerJsonToDict(items):
    ret = defaultdict(list)

    for item in items:
        player = dict()

        player["playerId"] = item["playerId"]["S"]
        player["money"] = item["money"]["N"]
        player["ownedMonsters"] = item["ownedMonsters"]["L"]
        player["lastLogin"] = item["lastLogin"]["S"]

        ret["players"].append(player)

    return ret


def mysfitJsonToDict(items):
    ret = defaultdict(list)

    for item in items:
        mysfit = dict()

        mysfit["monsterId"] = item["monsterId"]["S"]
        mysfit["masterId"] = item["masterId"]["S"]
        mysfit["food"] = item["food"]["N"]
        mysfit["entertainment"] = item["entertainment"]["N"]
        mysfit["level"] = item["level"]["N"]

        ret["monsters"].append(mysfit)

    return ret


def getPlayers():
    response = players.scan()

    return playerJsonToDict(response["Items"])


def getAllMonsters():
    response = owned_monsters.scan()

    return mysfitJsonToDict(response["Items"])


def getPlayerByID(id):
    response = players.get_item(Key={"playerId": id})

    return playerJsonToDict(response["Item"])


def getPlayersMonsters(masterId):
    response = owned_monsters.query(KeyConditionExpression=Key("masterId").eq(masterId))

    return mysfitJsonToDict(response["Items"])


def getMonsterByID(id, masterId):
    response = owned_monsters.get_item(Key={"masterId": masterId, "monsterId": id})

    return mysfitJsonToDict(response["Item"])
