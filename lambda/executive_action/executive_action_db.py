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


# Takes in executive action and respond with information or success code
# Note: does NOT handle special election; this is handled by next turn lambda
# @inputs
#	gameID
# 	executiveAction
#	playerID (if applicable)
# @outputs
# 	statusCode
# @updates
#	gameTable -> players
#	playerTable -> isAlive
def lambda_function(event, context=None):
	try:
		currentGameID = str(event['game_id'])
		executiveAction = event['executive_action']
	except:
		raise Exception('Error: Missing one or more parameters [99]')

	currentGame = get_game_info(currentGameID)
	gameTable = dynamodb.Table('secret-hitler-test')
	playerTable = dynamodb.Table('secret-hitler-players-test')
	returnValue = ""


	if executiveAction == 'policy_peek':

		returnValue = currentGame['deck'][0:3]

	elif executiveAction == 'investigate_loyalty':

		try:
			playerID = str(event['player_id'])
		except:
			raise Exception('Error: Player ID required for Investigation [500]')

		player = get_player_info(currentGameID, playerID)
		if player['role'] == 'L':
			returnValue = 'Liberal'
		else:
			returnValue = 'Facist'

	elif executiveAction == 'special_election':
		raise Exception('Error: Special Election should not be handled by this function')

	elif executiveAction == 'execution':
		try:
			playerID = str(event['player_id'])
		except:
			raise Exception('Error: Player ID required for Investigation [500]')


		player = get_player_info(currentGameID, playerID)

		if player['role'] == 'H':
			return "Liberals Win; Hitler is killed."

		player['isAlive'] = False

		index = None
		for i in range(0, len(currentGame['players'])):
			thisPlayerID = str(currentGame['players'][i]['playerID'])
			if thisPlayerID == playerID:
				index = i

		del currentGame['players'][index]


		resp = gameTable.update_item(
		        Key={"game": currentGameID},
		        UpdateExpression="set players = :pl",
		        ExpressionAttributeValues={
		            ':pl' : currentGame['players']
		})

		resp = playerTable.update_item(
		        Key={"gameID": currentGameID, "playerID": playerID },
		        UpdateExpression="set isAlive = :alive",
		        ExpressionAttributeValues={
		            ':alive' : player['isAlive']
		})

	return returnValue

