import json
import boto3
import random

dynamodb = boto3.resource('dynamodb')

# Given the number of players, return a randomized set of roles
def role_array(num_of_players):
    roles = []
    if (num_of_players == 5):
        roles.extend(['L', 'L', 'L', 'F', 'H'])
        num_liberals = 3
        num_facist = 2
    elif (num_of_players == 6):
        roles.extend(['L', 'L', 'L', 'L', 'F', 'H'])
        num_liberals = 4
        num_facist = 2
    elif (num_of_players == 7):
        roles.extend(['L', 'L', 'L', 'L', 'F', 'F', 'H'])
        num_liberals = 4
        num_facist = 3
    elif (num_of_players == 8):
        roles.extend(['L', 'L', 'L', 'L', 'L', 'F', 'F', 'H'])
        num_liberals = 5
        num_facist = 3
    elif (num_of_players == 9):
        roles.extend(['L', 'L', 'L', 'L', 'L', 'F', 'F', 'F', 'H'])
        num_liberals = 5
        num_facist = 4
    elif (num_of_players == 10):
        roles.extend(['L', 'L', 'L', 'L', 'L', 'L', 'F', 'F', 'F', 'H'])
        num_liberals = 6
        num_facist = 4
    else:
        roles = None
        num_liberals = None
        num_facist = None
    random.shuffle(roles)
    return (roles, num_liberals, num_facist)
        


def main(event, context):
    playersTable = dynamodb.Table('secret-hitler-players')
    gamesTable = dynamodb.Table('secret-hitler')
    num_of_players = int(event["num_of_players"])
    returnValue = {}
    
    # Game Set-up
    deck = ['L','L','L','L','L','L','F','F','F','F','F','F','F','F','F','F','F']
    random.shuffle(deck)
    print(deck)
    (roles,num_of_liberals,num_of_facist) = role_array(num_of_players)
    print(roles)
    
    
    # Add a game to game table (create deck & board)
    resp = gamesTable.scan(Select="COUNT")
    totalGames = resp["Count"]
    gameID = totalGames + 1
    resp = gamesTable.put_item(
        Item={
            'game' : str(gameID),
            'numberOfPlayers' : num_of_players,
            'numberOfLiberals' : num_of_liberals,
            'numberOfFacists': num_of_facist,
            'numberOfLiberalPolicies': 6,
            'numberOfFacistPolicies': 11,
            'numberOfLiberalPoliciesEnacted': 0,
            'numberOfFacistPoliciesEnacted': 0,
            'turn': 0,
            'players': [],
            'previousPresident': "Null",
            'previousChancellor': "Null"
        })
    
    # Enhancement
    # could delete old games
    # if totalcount = 0 add new record else get games older than x-time
    

    # Not needed anymore; Dropdown menu starts from 5-10
    # if (num_of_players < 5):
    #     raise Exception("Error: Not enough players")
    
    
    # create players
    for i in range(0,num_of_players):
        response = playersTable.put_item(
           Item={
                'playerID': str(i+1),
                'gameID': str(gameID),
                'isNull': True,
                'role': roles[i],
                'turn': 0
            }
        )
    
    # build deck & board based on number of players

    # print("PutItem succeeded:")
    returnValue["message"] = "Game successfully created."
    returnValue["data"] = { "game_id" : gameID }
    return returnValue