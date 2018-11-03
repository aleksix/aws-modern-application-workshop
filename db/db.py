from collections import defaultdict

import boto3

client = boto3.client("dynamodb")


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
    response = client.scan(
        TableName="MysfitsPlayers"
    )

    return playerJsonToDict(response["Items"])


def getAllMonsters():
    response = client.scan(
        TableName="MysfitsMonsters"
    )

    return mysfitJsonToDict(response["Items"])


def getPlayerByID(id):
    response = client.query(
        TableName="MysfitsPlayers",
        KeyConditions={"playerId": {"AttributeValueList": [{"N": id}],
                                    "ComparisonOperator": "EQ"}
                       }
    )

    return playerJsonToDict(response["Items"])


def getMonsterByID(id, masterId):
    pass
