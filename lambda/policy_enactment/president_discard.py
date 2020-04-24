import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
import pprint
pp = pprint.PrettyPrinter(indent=4)

import sys
sys.path.insert(1, '/Users/wingchungchow/Documents/programming_projects/secret_hitler/lambda/')
from aws_credentials import awsAccessKey, awsSecretKey, awsRegion


from helper import *


dynamodb = boto3.resource('dynamodb',  aws_access_key_id=awsAccessKey, aws_secret_access_key=awsSecretKey, region_name=awsRegion)


# @inputs
#   game_id String
#   discard String ('F' or 'L')
#   policies_in_hand ['F/L', 'F/L']

def lambda_handler(event, context=None):
    # TODO implement
    returnValue = {}
    
    try:
        currentGameID = str(event['game_id'])
        discard = str(event['discard'])
        policiesInHand = event['policies_in_hand']
    except:
        raise Exception('Error: Missing one or more parameters [99]')
    
    gameTable = dynamodb.Table('secret-hitler-test') # MARKER FOR LAMBDA DEPLOYMENT CHANGE
    returnValue = {}
    discard_list = []
    discard_list.append(discard)
    
    resp = gameTable.update_item(
        Key={"game": currentGameID},
        UpdateExpression="set discard = list_append(discard, :d), policiesInHand = :p",
        ExpressionAttributeValues={
            ':d' : discard_list,
            ':p' : policiesInHand
    })
	
	
    returnValue['message'] = "Successfully discarded card"
    returnValue['data'] = resp
	
    return returnValue