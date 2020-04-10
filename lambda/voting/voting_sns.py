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


def does_vote_pass(listOfVotes):
	yesCount = 0
	for vote in listOfVotes:
		if vote['vote']:
			yesCount = yesCount + 1

	return yesCount > .5 * len(listOfVotes)

def remove_previous_votes(table, gameID):
	gameID = str(gameID)
	playerTable = dynamodb.Table(table)
	resp = playerTable.query(
		KeyConditionExpression=Key('gameID').eq(gameID),
		FilterExpression=Attr('vote').exists()
	);
	players_with_votes = resp["Items"]

	while 'LastEvaluatedKey' in resp:
		resp = playerTable.scan(
			KeyConditionExpression=Key('gameID').eq(gameID),
			FilterExpression=Attr('vote').exists(),
			Limit=10, 
			ExclusiveStartKey=resp['LastEvaluatedKey'])
		players_with_votes.extend(resp['Items'])


	for player in players_with_votes:
		resp = playerTable.update_item(
			Key={"gameID": gameID, "playerID": player['playerID']},
			UpdateExpression="remove vote")



# Given the prez & chancellor ID, determine if vote passes
# @inputs
# 	gameID
#	presidentID - not necessary
#	chancellorID
# @outputs
# 	SNS readable data object case 1 (vote passes)
# 		- 3 policies from deck
# 		- Chancellor ID
#		- Veto Power
#	SNS readable data object case 2 (vote fails, electionTracker < 3)
#		- New President ID
# 		- Previous President ID
#		- Previous Chancellor ID 
# 		- Election Tracter  (int)
#		- List of players 
# 	SNS readable data object case 3 (vote fails, electionTracker = 3)
# 	Envoke End Game Lambda
# @updates
#	Dynamodb -> game table -> enacted policies
#		in the event of 3 fails
#	Dynamodb -> game table -> deck, previous office, currentPresidentID
#		passes & remove top 3 policies & update previous in office

def lambda_function(event, context=None):
	currentGameID = str(event['game_id'])
	chancellorID = str(event['chancellor_id'])
	playerTableName = 'secret-hitler-players-test'
	playerTable = dynamodb.Table(playerTableName)
	gameTable = dynamodb.Table('secret-hitler-test')

	currentGame = get_game_info(currentGameID)
	returnValue = {}

	# Collec Votes
	resp = playerTable.query(
		KeyConditionExpression=Key('gameID').eq(currentGameID),
		ProjectionExpression="vote"
	);
	votes = resp["Items"]
	while 'LastEvaluatedKey' in resp:
		resp = playerTable.query(
			ProjectionExpression="vote",
			KeyConditionExpression=Key('gameID').eq(currentGameID),
			Limit=10,
			ExclusiveStartKey=resp['LastEvaluatedKey'])
		votes.extend(resp['Items'])

	print("votes received")

	if does_vote_pass(votes):
		print('vote passes')
		# check to see if chancellor is hitler
		chancellor = get_player_info(currentGameID, chancellorID)
		if (chancellor['role'] == 'H' and int(currentGame['numberOfFacistPoliciesEnacted']) >= 3): 
			return 'Hitler'
		else:
			# get top 3 cards from deck
			deck = currentGame['deck']
			currentGame['policiesInHand'] = deck[0:3]
			del deck[0:3]
			currentGame['deck'] = deck
			currentGame['chancellorID'] = chancellorID 
			currentGame['electionTracker'] = 0

			# update game table
			# remove cards from deck; update previous office
			resp = gameTable.update_item(
		        Key={"game": currentGameID},
		        UpdateExpression="set deck = :dk, previousPresidentID = :prevPID, previousChancellorID = :prevCID, policiesInHand = :policies, electionTracker=:et",
		        ExpressionAttributeValues={
		            ':dk' : currentGame['deck'],
		            ':prevPID': currentGame['currentPresidentID'],
		            ':prevCID': currentGame['chancellorID'],
		            ':policies': currentGame['policiesInHand'],
		            ':et': currentGame['electionTracker']
			})

			# set return value to SNS topic
			returnValue['policiesInHand'] = currentGame['policiesInHand']
			returnValue['chancellorID'] = currentGame['chancellorID']
			returnValue['vetoPower'] = currentGame['vetoPower']

			
	else:
		currentPresidentID = currentGame['currentPresidentID']
		numberOfPlayers = currentGame['numberOfPlayers']
		listOfPlayers = currentGame['players']
		currentGame['currentPresidentID'] = next_president(currentPresidentID, numberOfPlayers, listOfPlayers)
		currentGame['electionTracker'] = int(currentGame['electionTracker']) + 1


		if currentGame['electionTracker'] == 3:
			print('flip over top card then assign new president')
			# enact top card from deck
			topCard = currentGame['deck'][0]
			del currentGame['deck'][0]

			if topCard == 'L':
				currentGame['numberOfLiberalPoliciesEnacted'] = currentGame['numberOfLiberalPoliciesEnacted'] + 1
			else:
				currentGame['numberOfFacistPoliciesEnacted'] = currentGame['numberOfFacistPoliciesEnacted'] + 1
				if currentGame['numberOfFacistPoliciesEnacted'] == 5:
					currentGame['vetoPower'] = True

			# Eliminate election restriction
			currentGame['previousPresidentID'] = "Null"
			currentGame['previousChancellorID'] = "Null"

			resp = gameTable.update_item(
				Key={"game": currentGameID},
		        UpdateExpression="set numberOfLiberalPoliciesEnacted = :lp, numberOfFacistPoliciesEnacted = :fp, deck = :dk, vetoPower = :vp, previousPresidentID=:prevPID, previousChancellorID=:prevCID",
		        ExpressionAttributeValues={
		            ':lp' : currentGame['numberOfLiberalPoliciesEnacted'] ,
		            ':fp': currentGame['numberOfFacistPoliciesEnacted'],
		            ':dk': currentGame['deck'],
		            ':vp': currentGame['vetoPower'],
		            ':prevPID': currentGame['previousPresidentID'],
		            ':prevCID': currentGame['previousChancellorID']
			})
			currentGame['electionTracker'] = 0


		# update database table with new president id, election tracker
		resp = gameTable.update_item(
				Key={"game": currentGameID},
		        UpdateExpression="set currentPresidentID = :cp, electionTracker = :et",
		        ExpressionAttributeValues={
		            ':cp' : currentGame['currentPresidentID'],
		            ':et':  currentGame['electionTracker']
			})


		returnValue['presidentID'] = str(currentGame['currentPresidentID'])
		returnValue['previousPresidentID'] = currentGame['previousPresidentID']
		returnValue['previousChancellorID'] = currentGame['previousChancellorID']
		returnValue['electionTracker'] = currentGame['electionTracker']
		returnValue['listOfPlayers'] = currentGame['players']

	remove_previous_votes(playerTableName, currentGameID)
	return returnValue