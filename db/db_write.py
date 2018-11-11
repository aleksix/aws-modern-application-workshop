from db.db import players, monsters


def add_player(playerId, money=100):
    # String set would make more sense, potentially, but I'm unsure if we can easily create it
    players.put_item(Item={
        "playerId": playerId,
        "money": money,
        "owned_monsters": list()
    })


def add_monster(playerId, monsterId, health=100, food=100, entertainment=100):
    monsters.put_item(Item={"masterId": playerId,
                            "monsterId": monsterId,
                            "health": health,
                            "food": food,
                            "entertainment": entertainment})
