import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
import pprint
import random
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
	gameTable = dynamodb.Table('secret-hitler-test') # MARKER FOR LAMBDA DEPLOYMENT
	playerTable = dynamodb.Table('secret-hitler-players-test') # MARKER FOR LAMBDA DEPLOYMENT
	returnValue = ""


	if executiveAction == 'policy_peek':

		if len(currentGame['deck']) <= 2:
			discard = currentGame['discard']
			random.shuffle(discard)

			currentGame['deck'].extend(discard)
			currentGame['discard'] = []

			resp = gameTable.update_item(
			    Key={"game": currentGameID},
			    UpdateExpression="set deck = :deck, discard = :discard",
			    ExpressionAttributeValues={
			        ':deck' : currentGame['deck'],
			        ':discard' : currentGame['discard']
			})

		currentGame['executiveActionResult'] = str(currentGame['deck'][0:3])

	elif executiveAction == 'investigate_loyalty':

		try:
			playerID = str(event['player_id'])
		except:
			raise Exception('Error: Player ID required for Investigation [500]')

		player = get_player_info(currentGameID, playerID)
		if player['role'] == 'L':
			currentGame['executiveActionResult'] = 'Liberal'
		else:
			currentGame['executiveActionResult'] = 'Facist'

	elif executiveAction == 'special_election':
		raise Exception('Error: Special Election should not be handled by this function')

	elif executiveAction == 'execution':
		try:
			playerID = str(event['player_id'])
		except:
			raise Exception('Error: Player ID required for Execution [500]')


		player = get_player_info(currentGameID, playerID)

		if player['role'] == 'H':

			currentGame['endGameStatus'] = 'L2'
			resp = gameTable.update_item(
			    Key={"game": currentGameID},
			    UpdateExpression="set endGameStatus = :endGame",
			    ExpressionAttributeValues={
			        ':endGame' : currentGame['endGameStatus']
			})


			event = {'end_game_status' : currentGame['endGameStatus'], 'game_id' : currentGameID}

			# MARKER FOR LAMBDA DEPLOYMENT
			# response = lambdaClient.invoke(
			# 	FunctionName='secret-hitler-end-game',
			# 	InvocationType='Event',
			# 	LogType='None',
			# 	Payload=json.dumps(event));
				
			currentGame['executiveActionResult'] = 'Hitler'
		else:
			currentGame['executiveActionResult'] = 'not Hitler'
		player['isAlive'] = False

		index = None
		for i in range(0, len(currentGame['players'])):
			thisPlayerID = str(currentGame['players'][i]['playerID'])
			if thisPlayerID == playerID:
				index = i

		executedPlayer = currentGame['players'].pop(index)
		currentGame['executedPlayers'].append(executedPlayer)


		resp = gameTable.update_item(
		        Key={"game": currentGameID},
		        UpdateExpression="set players = :pl, executedPlayers = :ep",
		        ExpressionAttributeValues={
		            ':pl' : currentGame['players'],
		            ':ep' : currentGame['executedPlayers']
		})

		resp = playerTable.update_item(
		        Key={"gameID": currentGameID, "playerID": playerID },
		        UpdateExpression="set isAlive = :alive",
		        ExpressionAttributeValues={
		            ':alive' : player['isAlive']
		})
	
	currentGame['executiveAction'] = 'Null'


	resp = gameTable.update_item(
	    Key={"game": currentGameID},
	    UpdateExpression="set executiveAction = :ea, executiveActionResult = :ear",
	    ExpressionAttributeValues={
	        ':ea' : currentGame['executiveAction'],
	        ':ear' : currentGame['executiveActionResult']
	})

	return currentGame['executiveActionResult']

