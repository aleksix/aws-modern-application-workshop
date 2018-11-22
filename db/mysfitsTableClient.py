import boto3
import json
import logging
from collections import defaultdict
from db.db_write import add_monster, add_player
import db.db
from datetime import datetime

# create a DynamoDB client using boto3. The boto3 library will automatically
# use the credentials associated with our ECS task role to communicate with
# DynamoDB, so no credentials need to be stored/managed at all by our code!
client = boto3.client('dynamodb')


def getAllMysfits():
    # Retrieve all Mysfits from DynamoDB using the DynamoDB scan operation.
    # Note: The scan API can be expensive in terms of latency when a DynamoDB
    # table contains a high number of records and filters are applied to the
    # operation that require a large amount of data to be scanned in the table
    # before a response is returned by DynamoDB. For high-volume tables that
    # receive many requests, it is common to store the result of frequent/common
    # scan operations in an in-memory cache. DynamoDB Accelerator (DAX) or
    # use of ElastiCache can provide these benefits. But, because out Mythical
    # Mysfits API is low traffic and the table is very small, the scan operation
    # will suit our needs for this workshop.
    response = client.scan(
        TableName='MysfitsTable'
    )

    logging.info(response["Items"])

    # loop through the returned mysfits and add their attributes to a new dict
    # that matches the JSON response structure expected by the frontend.
    mysfitList = defaultdict(list)
    for item in response["Items"]:
        mysfit = {}
        mysfit["mysfitId"] = item["MysfitId"]["S"]
        mysfit["name"] = item["Name"]["S"]
        mysfit["goodevil"] = item["GoodEvil"]["S"]
        mysfit["lawchaos"] = item["LawChaos"]["S"]
        mysfit["species"] = item["Species"]["S"]
        mysfit["thumbImageUri"] = item["ThumbImageUri"]["S"]
        mysfitList["mysfits"].append(mysfit)

    # convert the create list of dicts in to JSON
    return json.dumps(mysfitList)


def queryMysfits(queryParam):
    logging.info(json.dumps(queryParam))

    # Use the DynamoDB API Query to retrieve mysfits from the table that are
    # equal to the selected filter values.
    response = client.query(
        TableName='MysfitsTable',
        IndexName=queryParam['filter'] + 'Index',
        KeyConditions={
            queryParam['filter']: {
                'AttributeValueList': [
                    {
                        'S': queryParam['value']
                    }
                ],
                'ComparisonOperator': "EQ"
            }
        }
    )

    mysfitList = defaultdict(list)
    for item in response["Items"]:
        mysfit = {}
        mysfit["mysfitId"] = item["MysfitId"]["S"]
        mysfit["name"] = item["Name"]["S"]
        mysfit["goodevil"] = item["GoodEvil"]["S"]
        mysfit["lawchaos"] = item["LawChaos"]["S"]
        mysfit["species"] = item["Species"]["S"]
        mysfit["thumbImageUri"] = item["ThumbImageUri"]["S"]
        mysfitList["mysfits"].append(mysfit)

    return json.dumps(mysfitList)


# Retrive a single mysfit from DynamoDB using their unique mysfitId
def getMysfit(mysfitId):
    # use the DynamoDB API GetItem, which gives you the ability to retrieve
    # a single item from a DynamoDB table using its unique key with super
    # low latency.
    response = client.get_item(
        TableName='MysfitsTable',
        Key={
            'MysfitId': {
                'S': mysfitId
            }
        }
    )

    item = response["Item"]

    mysfit = {}
    mysfit["mysfitId"] = item["MysfitId"]["S"]
    mysfit["name"] = item["Name"]["S"]
    mysfit["age"] = int(item["Age"]["N"])
    mysfit["goodevil"] = item["GoodEvil"]["S"]
    mysfit["lawchaos"] = item["LawChaos"]["S"]
    mysfit["species"] = item["Species"]["S"]
    mysfit["description"] = item["Description"]["S"]
    mysfit["thumbImageUri"] = item["ThumbImageUri"]["S"]
    mysfit["profileImageUri"] = item["ProfileImageUri"]["S"]
    mysfit["likes"] = item["Likes"]["N"]
    mysfit["adopted"] = item["Adopted"]["BOOL"]

    return json.dumps(mysfit)


# increment the number of likes for a mysfit by 1
def likeMysfit(mysfitId):
    # Use the DynamoDB API UpdateItem to increment the number of Likes
    # the mysfit has by 1 using an UpdateExpression.
    response = client.update_item(
        TableName='MysfitsTable',
        Key={
            'MysfitId': {
                'S': mysfitId
            }
        },
        UpdateExpression="SET Likes = Likes + :n",
        ExpressionAttributeValues={':n': {'N': '1'}}
    )

    response = {}
    response["Update"] = "Success";

    return json.dumps(response)


# assign a mysfit to a player
def adoptMysfit(mysfitId, playerId, cost):
    response = {}
    response["Update"] = "Failure"

    money = db.db.getPlayerByID(playerId)["players"][0]["money"]

    result = (money < cost)

    if not result:
        return json.dumps(response)

    result = add_monster(playerId, mysfitId)

    if not result:
        return json.dumps(response)

    db.db.players.update_item(Key={"playerId": playerId},
                              AttributeUpdates={
                                  "money": {"Value": money - cost,
                                            "Action": "PUT"}})

    response["Update"] = "Success";

    return json.dumps(response)


# Create or update the player data
def confirmPlayer(playerId):
    add_player(playerId)

    response = {}
    response["Update"] = "Success";

    return json.dumps(response)


# Save data from the player's game
def save(playerId, money, monsterData):
    db.db.players.update_item(Key={"playerId": playerId},
                              AttributeUpdates={
                                  "lastLogin": {"Value": datetime.utcnow().isoformat(),
                                                "Action": "PUT"},
                                  "money": {"Value": int(money),
                                            "Action": "PUT"}})

    for monster in monsterData:
        db.db.owned_monsters.update_item(Key={"masterId": playerId, "monsterId": monster["monsterId"]},
                                         AttributeUpdates={
                                             "food": {"Value": monster["food"],
                                                      "Action": "PUT"},
                                             "entertainment": {"Value": monster["entertainment"],
                                                               "Action": "PUT"},
                                             "level": {"Value": monster["level"],
                                                       "Action": "PUT"}})

    response = {}
    response["Update"] = "Success";

    return json.dumps(response)


def retrieve(playerId):
    response = {}

    player = db.db.getPlayerByID(playerId)["players"][0]

    # We don't need to send the owned monsters or the ID
    del player["ownedMonsters"]
    del player["playerId"]

    response["player"] = player

    monsters = db.db.getPlayersMonsters(playerId)["monsters"]

    for c in range(len(monsters)):
        del monsters[c]["monsterId"]
        del monsters[c]["masterId"]

    response["monsters"] = monsters

    response["Update"] = "Success";

    return json.dumps(response)
