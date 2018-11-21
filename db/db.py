from collections import defaultdict
from boto3.dynamodb.conditions import Key, Attr
import boto3

client = boto3.client("dynamodb")

dynamodb = boto3.resource("dynamodb")

players = dynamodb.Table("MysfitsPlayers")
owned_monsters = dynamodb.Table("MysfitsMonsters")


def playerJsonToDict(items):
    ret = defaultdict(list)

    for item in items:
        player = {}

        player["playerId"] = item["playerId"]["N"]
        player["money"] = item["money"]["N"]
        player["monsters"] = item["monsters"]["NS"]

        ret["players"].append(player)

    return ret


def mysfitJsonToDict(items):
    ret = defaultdict(list)

    for item in items:
        mysfit = {}

        mysfit["monsterId"] = mysfit["monsterId"]["N"]
        mysfit["masterId"] = mysfit["masterId"]["N"]
        mysfit["health"] = mysfit["health"]["N"]
        mysfit["food"] = mysfit["food"]["N"]
        mysfit["entertainment"] = mysfit["entertainment"]["N"]

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


if __name__ == "__main__":
    # Testing code
    pass
