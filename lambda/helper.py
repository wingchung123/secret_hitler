import boto3
from boto3.dynamodb.conditions import Key, Attr
import random
import json
import pprint
pp = pprint.PrettyPrinter(indent=4)


import sys
sys.path.insert(1, '/Users/wingchungchow/Documents/programming_projects/secret_hitler/lambda/')
from aws_credentials import awsAccessKey, awsSecretKey, awsRegion

dynamodb = boto3.resource('dynamodb',  aws_access_key_id=awsAccessKey, aws_secret_access_key=awsSecretKey, region_name=awsRegion)


def get_game_info(gameID):
    gameTable = dynamodb.Table('secret-hitler-test')
    currentGame = None

    resp = gameTable.get_item(Key={
            "game": str(gameID)
        })
    
    if "Item" in resp:
        currentGame = resp["Item"]
    else:
        # there's no item in the table with this game ID
        print("no matching game")


    # pp.pprint(currentGame)
    return currentGame


def get_player_info(gameID, playerID):
    playerTable = dynamodb.Table('secret-hitler-players-test')
    playerInfo = None

    resp = playerTable.get_item(Key={
        "gameID": str(gameID),
        "playerID" : str(playerID)
    })

    if "Item" in resp:
        playerInfo = resp["Item"]
    else:
        # there's no item in the table with this game ID
        print("no matching player & game ID combo")


    print(playerInfo)
    return playerInfo


def create_test_player(playerID="default_test", gameID="default_test", isNull=False,role='L', turn=0, playerName='no_name', vote=None):
    
    if (isNull):
        Item={
        'playerID': playerID,
        'gameID': gameID,
        'isNull': isNull,
        'role': role,
        'turn': turn
        }
    elif vote is None:
        Item={
        'playerID': playerID,
        'gameID': gameID,
        'isNull': isNull,
        'role': role,
        'turn': turn,
        'playerName': playerName
        }
    else: 
        Item={
        'playerID': playerID,
        'gameID': gameID,
        'isNull': isNull,
        'role': role,
        'turn': turn,
        'playerName': playerName,
        'vote': vote
        }
    return Item


# Copied from secret_hitler_start_game
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
        
def create_test_game(numberOfPlayers=5, gameID="default_test", numberOfLiberalPoliciesEnacted=0,
    numberOfFacistPoliciesEnacted=0, turn=0, players=[], currentPresidentID="Null", currentChancellorID="Null",
    previousPresidentID="Null", previousChancellorID="Null", electionTracker=0, vetoPower=False, 
    policiesInHand=[], deck=[], discard=[],
    executedPlayers=[], executiveAction="Null", endGameStatus="Null",
    specialElectionPresidentPlaceholder="Null",executiveActionResult="Null"):

    if deck == []:
        deck = ['L','L','L','L','L','L','F','F','F','F','F','F','F','F','F','F','F']
        random.shuffle(deck)

    if players != []:
        for player in players:
            player['playerID'] = int(player['playerID'])


    (roles, numberOfLiberals, numberOfFacists) = role_array(numberOfPlayers)
    Item={
        'game' : str(gameID),
        'numberOfPlayers' : numberOfPlayers,
        'numberOfLiberals' : numberOfLiberals,
        'numberOfFacists': numberOfFacists,
        'numberOfLiberalPolicies': 6,
        'numberOfFacistPolicies': 11,
        'numberOfLiberalPoliciesEnacted': numberOfLiberalPoliciesEnacted,
        'numberOfFacistPoliciesEnacted': numberOfFacistPoliciesEnacted,
        'turn': turn,
        'players': players,
        'currentPresidentID': currentPresidentID,
        'currentChancellorID' : currentChancellorID,
        'previousPresidentID': previousPresidentID,
        'previousChancellorID': previousChancellorID,
        'electionTracker': electionTracker,
        'vetoPower': vetoPower,
        'policiesInHand' : policiesInHand,
        'deck': deck,
        'discard': discard,
        'executedPlayers' : executedPlayers,
        'executiveAction' : executiveAction,
        'endGameStatus' : endGameStatus,
        'specialElectionPresidentPlaceholder' : specialElectionPresidentPlaceholder,
        'executiveActionResult' : executiveActionResult
    }

    return Item



def is_player_alive(playerID, listOfPlayers):

    for player in listOfPlayers:
        alivePlayerID = str(player['playerID'])
        if alivePlayerID == str(playerID):
            return True

    return False




# Note: Number of Players != len(listOfPlayers)
#       - Case: if someone is killed, you still need to mod by original # of players
def next_president(currentPresidentID, numberOfPlayers, listOfPlayers):
    # make sure to check the player is alive

    if len(listOfPlayers) == 0:
        return -1000 # maybe change to a more invalid value

    newPresidentID = (int(currentPresidentID) + 1) % numberOfPlayers
    if newPresidentID == 0:
        newPresidentID = numberOfPlayers

    isAlive = is_player_alive(newPresidentID, listOfPlayers)
    while not isAlive:
        newPresidentID = (newPresidentID + 1) % numberOfPlayers
        if newPresidentID == 0:
            newPresidentID = numberOfPlayers
        isAlive = is_player_alive(newPresidentID, listOfPlayers)

    return str(newPresidentID)



