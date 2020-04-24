import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
import pprint
pp = pprint.PrettyPrinter(indent=4)

import sys
sys.path.insert(1, '/Users/wingchungchow/Documents/programming_projects/secret_hitler/lambda/')
from aws_credentials import awsAccessKey, awsSecretKey, awsRegion


from helper import *

# MARKER FOR LAMBDA DEPLOYMENT
dynamodb = boto3.resource('dynamodb',  aws_access_key_id=awsAccessKey, aws_secret_access_key=awsSecretKey, region_name=awsRegion)
lambdaClient = boto3.client('lambda', aws_access_key_id=awsAccessKey, aws_secret_access_key=awsSecretKey, region_name=awsRegion)

# Publishes a message to SNS topic to alert players & start next turn
# Does NOT write to dynamoDB
# @inputs
# 	gameID
#	presidentID
# @outputs
# 	SNS readable data object
# 		- Presdient Player ID
# 		- Previous President ID
#		- Previous Chancellor ID 
# 		- Election Tracter  (int)
#		- List of players 
def lambda_function(event, context=None):
	
	currentGameID = str(event['game_id'])
	gameTable = dynamodb.Table('secret-hitler-test') #MARKER CHANGE FOR LAMBDA DEPLOYMENT

	returnValue = {
		"presidentID": "",
		"previousPresidentID": "",
		"previousChancellorID": "",
		"electionTracker": 0,
		"listOfPlayers": [], # must be list of maps/dicts of playerIDs & playerNames
		"executedPlayers" : [],
		"gameID" : currentGameID,
		"vetoPower" : ""
	}

	currentGame = get_game_info(currentGameID)
	pp.pprint(currentGame)
	# print(currentGame)

	# Clear out Chancellor ID & Executive Action Result
	currentGame['currentChancellorID'] = 'Null'
	currentGame['executiveActionResult'] = 'Null'
	
	if 'president_id' not in event:

		if(currentGame['specialElectionPresidentPlaceholder'] != 'Null'):
			currentGame["currentPresidentID"] = currentGame['specialElectionPresidentPlaceholder']
			currentGame['specialElectionPresidentPlaceholder'] = 'Null'
		

		if (currentGame["currentPresidentID"] != 'Null'):
			# president exists; increment mod number of players
			# make sure to check the player is alive
			currentPresidentID = currentGame['currentPresidentID']
			numberOfPlayers = currentGame['numberOfPlayers']
			players = currentGame['players']

			currentGame["currentPresidentID"] = next_president(currentPresidentID, numberOfPlayers,players)

		else:
			# no president; start with president id = 1
			currentGame["currentPresidentID"]  = '1'
	else:
		# print("there is a president ID")
		currentGame['specialElectionPresidentPlaceholder'] = str(currentGame['currentPresidentID']) # do this to return a new object and avoid aliasing
		currentGame['currentPresidentID'] = str(event['president_id'])
		# clear out executive action
		currentGame['executiveAction'] = 'Null'



	# don't write to db so if special election fails it runs it back to original order
	resp = gameTable.update_item(
		Key={"game": currentGameID},
		UpdateExpression="set currentPresidentID = :cp, specialElectionPresidentPlaceholder = :se, currentChancellorID = :cid, executiveAction = :ea, executiveActionResult = :ear",
		ExpressionAttributeValues={
			':cp' : currentGame['currentPresidentID'],
			':se' : currentGame['specialElectionPresidentPlaceholder'],
			':cid' :  currentGame['currentChancellorID'],
			':ea' : currentGame['executiveAction'],
			':ear' : currentGame['executiveActionResult']
	})

	# set up return value
	returnValue['presidentID'] = str(currentGame["currentPresidentID"])
	returnValue['previousPresidentID'] = str(currentGame['previousPresidentID'])
	returnValue['previousChancellorID'] = str(currentGame['previousChancellorID'])
	returnValue['electionTracker'] = int(currentGame['electionTracker'])
	returnValue['listOfPlayers'] = currentGame['players']
	returnValue['executedPlayers'] = currentGame['executedPlayers']
	returnValue['specialElectionPresidentPlaceholder'] = currentGame['specialElectionPresidentPlaceholder']
	returnValue['chancellorID'] = currentGame['currentChancellorID']
	returnValue['vetoPower'] = currentGame['vetoPower']
	returnValue['executiveActionResult'] = currentGame['executiveActionResult']
	returnValue['executiveAction'] = currentGame['executiveAction']
	returnValue['numberOfFacistPoliciesEnacted'] = int(currentGame['numberOfFacistPoliciesEnacted'])
	returnValue['numberOfLiberalPoliciesEnacted'] = int(currentGame['numberOfLiberalPoliciesEnacted'])
	
	publishEvent = {
		'subject' : 'next_turn',
		'payload' : returnValue
	}

	# MARKER CHANGE FOR LAMBDA DEPLOYMENT
	# response = lambdaClient.invoke(
	# 	FunctionName='secret-hitler-sns-publish',
	# 	InvocationType='Event', # set to Event for async (no response req.)
	# 	LogType='None',
	# 	Payload=json.dumps(publishEvent)
	# )
	
	# returnValue = {}
	# returnValue["message"] = "Success in calling next turn."
	# returnValue["data"] = ""

	return returnValue