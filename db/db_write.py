from db.db import players, owned_monsters
from botocore.exceptions import ClientError


def add_player(playerId, money=100):
    # String set would make more sense, potentially, but I'm unsure if we can easily create it
    players.put_item(Item={
        "playerId": playerId,
        "money": money,
        "owned_monsters": list()
    })
    return True


def add_monster(playerId, monsterId, health=100, food=100, entertainment=100):
    playerData = players.get_item(Key={"playerId": playerId})
    if "Item" not in playerData:
        return False
    owned_monsters.put_item(Item={"masterId": playerId,
                                  "monsterId": monsterId,
                                  "health": health,
                                  "food": food,
                                  "entertainment": entertainment})
    players.update_item(Key={"playerId": playerId},
                        AttributeUpdates={
                            "owned_monsters": {"Value": list(monsterId),
                                               "Action": "ADD"}})
    return True
