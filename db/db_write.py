from db.db import players, owned_monsters
from datetime import datetime


def add_player(playerId, money=100):
    # String set would make more sense, potentially, but I'm unsure if we can easily create it
    playerData = players.get_item(Key={"playerId": playerId})
    if "Item" in playerData:
        return False

    lastLogin = datetime.utcnow().isoformat()
    players.put_item(Item={
        "playerId": playerId,
        "money": money,
        "ownedMonsters": list(),
        "lastLogin": lastLogin
    })
    return True


def add_monster(playerId, monsterId, food=100, entertainment=100, level=1):
    playerData = players.get_item(Key={"playerId": playerId})
    if "Item" not in playerData:
        return False

    owned_monsters.put_item(Item={"masterId": playerId,
                                  "monsterId": monsterId,
                                  "food": food,
                                  "entertainment": entertainment,
                                  "level": level})
    
    players.update_item(Key={"playerId": playerId},
                        AttributeUpdates={
                            "ownedMonsters": {"Value": list(monsterId),
                                              "Action": "ADD"}})
    return True
