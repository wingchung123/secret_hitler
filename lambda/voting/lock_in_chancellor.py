import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
import pprint
pp = pprint.PrettyPrinter(indent=4)

dynamodb = boto3.resource('dynamodb') # MARKER CHANGE FOR LAMBDA DEPLOY

def lambda_handler(event, context):
    # TODO implement
    returnValue = {}
    
    try:
        currentGameID = str(event['game_id'])
        chancellorID = str(event['chancellor_id'])
    except:
        raise Exception('Error: Missing one or more parameters [99]')
    
    gameTable = dynamodb.Table('secret-hitler')
    returnValue = {}
    
    resp = gameTable.update_item(
        Key={"game": currentGameID},
        UpdateExpression="set currentChancellorID = :c",
        ExpressionAttributeValues={
            ':c' : chancellorID
    })
	
	
    returnValue['message'] = "Successfully selected chancellor"
    returnValue['data'] = resp
	
    return returnValue