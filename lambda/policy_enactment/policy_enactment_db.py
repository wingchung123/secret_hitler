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
lambdaClient = boto3.client('lambda',  aws_access_key_id=awsAccessKey, aws_secret_access_key=awsSecretKey, region_name=awsRegion)






def return_executive_action(numberOfPlayers, numberOfFacistPoliciesEnacted):
	index = {
	"small": ['Null', 'Null', 'policy_peek', 'execution', 'execution', 'Null'],
	"medium": ['Null', 'investigate_loyalty', 'special_election', 'execution', 'execution', 'Null'],
	"large": ['investigate_loyalty', 'investigate_loyalty', 'special_election', 'execution', 'execution', 'Null']
	}

	if numberOfPlayers < 7:
		return index['small'][int(numberOfFacistPoliciesEnacted) - 1]
	elif numberOfPlayers < 9:
		return index['medium'][int(numberOfFacistPoliciesEnacted) - 1]
	else:
		return index['large'][int(numberOfFacistPoliciesEnacted) - 1]


# Writes to DB the policies to enact/discard
# @inputs
# 	enact string ex. 'F'
#	discard string ex. 'L'
#	gameID
# @outputs
# 	executive action (if any)
# @updates
#	gameTable -> numberOfFacistPoliciesEnacted,numberOfLiberalPoliciesEnacted, deck, discard
def lambda_function(event, context=None):
	try:
		currentGameID = str(event['game_id'])
		discard = event['discard']
		enactPolicy = event['enact']
	except:
		raise Exception('Error: Missing one or more parameters [99]')

	currentGame = get_game_info(currentGameID)
	gameTable = dynamodb.Table('secret-hitler-test') #MARKER CHANGE FOR LAMBDA DEPLOYMENT
	event = ""

	# Make updates to database object & update to database
	# Enact policy
	if enactPolicy == 'L':
		currentGame['numberOfLiberalPoliciesEnacted'] = currentGame['numberOfLiberalPoliciesEnacted'] + 1
	elif enactPolicy == 'F':
		currentGame['numberOfFacistPoliciesEnacted'] = currentGame['numberOfFacistPoliciesEnacted'] + 1

	# Check Veto Power
	if currentGame['numberOfFacistPoliciesEnacted'] == 5:
		currentGame['vetoPower'] = True


	# Check end game status
	if currentGame['numberOfFacistPoliciesEnacted'] == 6:
		print('Facist Win')
		currentGame['endGameStatus'] = 'F1'
	elif currentGame['numberOfLiberalPoliciesEnacted'] == 5:
		print('Liberals Win')
		currentGame['endGameStatus'] = 'L1'
		

	# Check Executive Action ONLY IF FACIST POLICY IS PASSED
	if (enactPolicy == 'F'):
		currentGame['executiveAction'] = return_executive_action(currentGame['numberOfPlayers'], currentGame['numberOfFacistPoliciesEnacted'])



	# Update Discard & Deck (Check if veto power was enacted)
	# Put discard in discard pile and shuffle if necessary
	if enactPolicy == 'Null': #discard entire hand
		currentGame['discard'].extend(currentGame['policiesInHand'])
	else:
		currentGame['discard'].append(discard)
	currentGame['policiesInHand'] = [] # empty out policies in hand

	if len(currentGame['deck']) <= 2:
		discard = currentGame['discard']
		random.shuffle(discard)

		currentGame['deck'].extend(discard)
		currentGame['discard'] = []

	# Update DB with above changed values
	resp = gameTable.update_item(
			Key={"game": currentGameID},
			UpdateExpression="set numberOfLiberalPoliciesEnacted = :lp, numberOfFacistPoliciesEnacted = :fp, vetoPower = :vp, policiesInHand = :pih, deck = :dk, discard = :discard, executiveAction = :ea, endGameStatus = :endgame",
			ExpressionAttributeValues={
				':lp' : currentGame['numberOfLiberalPoliciesEnacted'],
				':fp' : currentGame['numberOfFacistPoliciesEnacted'],
				':vp' : currentGame['vetoPower'],
				':pih' : currentGame['policiesInHand'],
				':dk' : currentGame['deck'],
				':discard' : currentGame['discard'],
				':ea' : currentGame['executiveAction'],
				':endgame' : currentGame['endGameStatus']
	})



	# Next Step
	# If end game, then send end game sns, if executive action, then send policy enact sns else send next turn sns
	if (currentGame['numberOfFacistPoliciesEnacted'] == 6 or currentGame['numberOfLiberalPoliciesEnacted'] == 5):
		print('End of Game')
		event = {'end_game_status' : currentGame['endGameStatus'], 'game_id' : currentGameID}

		# MARKER FOR LAMBDA DEPLOYMENT
		# response = lambdaClient.invoke(
		# 	FunctionName='secret-hitler-end-game',
		# 	InvocationType='Event',
		# 	LogType='None',
		# 	Payload=json.dumps(event));

	elif currentGame['executiveAction'] != 'Null':
		snsPayload = {
			"gameID" : currentGameID,
			"numberOfFacistPoliciesEnacted" : int(currentGame['numberOfFacistPoliciesEnacted']),
			"numberOfLiberalPoliciesEnacted" : int(currentGame['numberOfLiberalPoliciesEnacted']),
			# "vetoPower" : currentGame['vetoPower'],
			"executiveAction" : currentGame['executiveAction']
		}
		event = {
			'subject' : 'policy_enactment',
			'payload' : snsPayload
		}

		# MAKRER FOR LAMBDA DEPLOYMENT
		# response = lambdaClient.invoke(
		# 	FunctionName='secret-hitler-sns-publish',
		# 	InvocationType='Event', # set to Event for async (no response req.)
		# 	LogType='None',
		# 	Payload=json.dumps(event)
		# )

	else:
		event = {
			'game_id' : currentGameID
		}

		response = lambdaClient.invoke(
			FunctionName='secret-hitler-next-turn',
			InvocationType='RequestResponse', # set to Event for async MARKER FOR LAMBDA DEPLOYMENT
			LogType='None',
			Payload=json.dumps(event)
		)
		

	return event

