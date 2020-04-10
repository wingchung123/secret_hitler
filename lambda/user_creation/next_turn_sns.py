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
	gameTable = dynamodb.Table('secret-hitler-test')

	returnValue = {
		"presidentID": "",
		"prevPresidentID": "",
		"prevChancellorID": "",
		"electionTracker": 0,
		"listOfPlayers": [] # must be list of maps/dicts of playerIDs & playerNames
	}

	currentGame = get_game_info(currentGameID)
	pp.pprint(currentGame)
	# print(currentGame)
	
	if 'president_id' not in event:

		newPresidentID = None

		if (currentGame["currentPresidentID"] != 'Null'):
			# president exists; increment mod number of players
			# make sure to check the player is alive
			currentPresidentID = currentGame['currentPresidentID']
			numberOfPlayers = currentGame['numberOfPlayers']
			players = currentGame['players']

			newPresidentID = next_president(currentPresidentID, numberOfPlayers,players)

		else:
			# no president; start with president id = 1
			newPresidentID  = '1'

		# set up return value
		returnValue['presidentID'] = str(newPresidentID)
		returnValue['previousPresidentID'] = str(currentGame['previousPresidentID'])
		returnValue['previousChancellorID'] = str(currentGame['previousChancellorID'])
		returnValue['electionTracker'] = int(currentGame['electionTracker'])
		returnValue['listOfPlayers'] = currentGame['players']


		# needs to write to db the current president ID
		resp = gameTable.update_item(
				Key={"game": currentGameID},
		        UpdateExpression="set currentPresidentID = :cp",
		        ExpressionAttributeValues={
		            ':cp' : newPresidentID
			})


	else:
		# print("there is a president ID")
		specialElectionID = event['president_id']
		returnValue['presidentID'] = str(specialElectionID)
		returnValue['previousPresidentID'] = str(currentGame['previousPresidentID'])
		returnValue['previousChancellorID'] = str(currentGame['previousChancellorID'])
		returnValue['electionTracker'] = int(currentGame['electionTracker'])
		returnValue['listOfPlayers'] = currentGame['players']

		# don't write to db so if special election fails it runs it back to original ordre

	return returnValue


# event={
# 	"gameID" : "3"
# }

#pp.pprint(lambda_function(event))


