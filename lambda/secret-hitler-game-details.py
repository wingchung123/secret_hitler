import json
import boto3
from boto3.dynamodb.conditions import Key, Attr



dynamodb = boto3.resource('dynamodb')

def main(event, context):

    table_type = event["table"]
    game_id = event["game_id"]
    
    if table_type == 'game':
        table = dynamodb.Table('secret-hitler')
        resp = table.get_item(Key={
            "game": game_id
        })
    elif table_type == 'player':
        player_id = event["player_id"]
        table = dynamodb.Table('secret-hitler-players')
        resp = table.get_item(Key={
            "gameID": game_id,
            "playerID" : player_id
        })
    returnValue = {}
    
    if "Item" in resp:
        print(resp["Item"])
        returnValue["message"] = "Id found in %s table. Details in payload." % table_type
        returnValue["data"] = resp["Item"]
        return returnValue
    else:
        raise Exception("Error: No matching ID in %s table. [120]" % table_type)
