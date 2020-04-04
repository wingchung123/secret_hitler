import json
import boto3
from boto3.dynamodb.conditions import Key, Attr


dynamodb = boto3.resource('dynamodb')

def main(event, context):
        
    playerName = event["player_name"]
    gameID = event["game_id"]
    MAX_RETRIES = 3
    table = dynamodb.Table('secret-hitler-players')
    returnValue = {}
    
    resp = table.scan(FilterExpression=Attr('gameID').eq(gameID), ProjectionExpression="playerName", Limit=10)
    existing_player_list = resp["Items"]

    while 'LastEvaluatedKey' in resp:
        resp = table.scan(FilterExpression=Attr('gameID').eq(gameID), ProjectionExpression="playerName", Limit=10, ExclusiveStartKey=resp['LastEvaluatedKey'])
        existing_player_list.extend(resp['Items'])

    names = []
    if existing_player_list:
        for player in existing_player_list:
            if "playerName" in player:
                names.append(player["playerName"])
        print(names)
    
    if playerName in names:
        raise Exception("Error: Another player already has this name. Please choose another name. [110]")
 
    
    i = 0
    successful = False
    player_id = None
    while i < 3 and not successful:
        i = i + 1
        resp = table.scan(FilterExpression=Attr('isNull').eq(True) & Attr('gameID').eq(gameID), Limit=10)
        print(resp)
        player_list = resp["Items"]

        while 'LastEvaluatedKey' in resp and not player_list:
            resp = table.scan(FilterExpression=Attr('isNull').eq(True) & Attr('gameID').eq(gameID), Limit=10, ExclusiveStartKey=resp['LastEvaluatedKey'])
            player_list.extend(resp['Items'])
        
        if not player_list:
            raise Exception("Error: No more player ids left... Please start a new game if not all players are in. [111]")
            
        try:
            for player in player_list:
                resp = table.update_item(
                    Key={'playerID': player["playerID"], "gameID": gameID},
                    UpdateExpression="set playerName = :pn, isNull = :null",
                    ExpressionAttributeValues={
                        ':pn' : playerName,
                        ':null' : False
                    },
                    ConditionExpression=Attr('playerName').not_exists())
                player_id = player["playerID"]
                break
            
            # if it gets to here, it is successful
            successful = True
        except Exception as e:
            raise Exception("Error: Possible conflicting updates... Trying again. If this is the error message, check database to ensure data is valid i.e. players with names have isNull as false.")
            print(e)
        
    
    if successful:
        # update game table; append player name
        gameTable = dynamodb.Table('secret-hitler')
        resp = gameTable.update_item(
            Key={"game": gameID},
            UpdateExpression="set players = list_append(players, :player)",
            ExpressionAttributeValues ={
                ':player': [playerName]
            })

        returnValue["message"] = "Player successfully added."
        returnValue["data"] = { "player_id": player_id }
        return returnValue
    else:
        raise Exception("Error: Maximum retires reached... Player could not be added. [112]")
