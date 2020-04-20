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


# Given a gameID, check to see if all players' votes are in
def checkPlayersVotesAreReady(gameID):
	playerTable = dynamodb.Table('secret-hitler-players-test')
	resp = playerTable.query(
		KeyConditionExpression=Key('gameID').eq(gameID),
		FilterExpression=Attr('vote').not_exists() & Attr('isAlive').not_exists()
	);
	players_without_votes = resp["Items"]

	while 'LastEvaluatedKey' in resp:
		resp = playerTable.query(
			KeyConditionExpression=Key('gameID').eq(gameID),
			FilterExpression=Attr('vote').not_exists() & Attr('isAlive').not_exists(),
			Limit=10, 
			ExclusiveStartKey=resp['LastEvaluatedKey'])
		players_without_votes.extend(resp['Items'])

	print(players_without_votes)
	return players_without_votes == []




# Writes to DB the vote for specific president & chancellor combination
# @inputs
# 	game_id
#	player_id
#	president_id
# 	chancellor_id
# 	vote
# @outputs
# 	statusCode
# @updates
#	playerTable -> vote
def lambda_function(event, context=None):
	try:
		currentGameID = str(event['game_id'])
		playerID = str(event['player_id'])
		presidentID = str(event['president_id'])
		chancellorID = str(event['chancellor_id'])
		vote = event['vote']
	except:
		raise Exception('Error: Missing one or more parameters [99]')

	playerTable = dynamodb.Table('secret-hitler-players-test')

	resp = playerTable.update_item(
	        Key={'playerID': playerID, "gameID": currentGameID},
	        UpdateExpression="set vote = :vt",
	        ExpressionAttributeValues={
	            ':vt' : vote
	})



