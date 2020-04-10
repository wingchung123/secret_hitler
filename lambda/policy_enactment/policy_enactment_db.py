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

def return_executive_action(numberOfPlayers, numberOfFacistPoliciesEnacted):
	index = {
	"small": ['', '', 'policy peek', 'execution', 'execution', ''],
	"medium": ['', 'investigate loyalty', 'special election', 'execution', 'execution', ''],
	"large": ['investigate loyalty', 'investigate loyalty', 'special election', 'execution', 'execution', '']
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
#	discard list ex. ['L', 'F']
#	gameID
# @outputs
# 	statusCode
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
	gameTable = dynamodb.Table('secret-hitler-test')
	returnValue = ""


	# Enact policy
	if enactPolicy == 'L':
		currentGame['numberOfLiberalPoliciesEnacted'] = currentGame['numberOfLiberalPoliciesEnacted'] + 1
	else:
		currentGame['numberOfFacistPoliciesEnacted'] = currentGame['numberOfFacistPoliciesEnacted'] + 1

	# Check Veto Power
	if currentGame['numberOfFacistPoliciesEnacted'] == 5:
		currentGame['vetoPower'] = True

	# Check End Game criteria
	if currentGame['numberOfFacistPoliciesEnacted'] == 6:
		print('Facist Win')
		returnValue = 'Facist Win'
	elif currentGame['numberOfLiberalPoliciesEnacted'] == 5:
		print('Liberals Win')
		returnValue = 'Liberals Win'
	else:
		returnValue = return_executive_action(currentGame['numberOfPlayers'], currentGame['numberOfFacistPoliciesEnacted'])


	# Put discard in discard pile and shuffle if necessary
	currentGame['discard'].extend(discard)
	currentGame['policiesInHand'] = [] # empty out policies in hand

	if len(currentGame['deck']) <= 2:
		discard = currentGame['discard']
		random.shuffle(discard)

		currentGame['deck'].extend(discard)
		currentGame['discard'] = []



	resp = gameTable.update_item(
	        Key={"game": currentGameID},
	        UpdateExpression="set numberOfLiberalPoliciesEnacted = :lp, numberOfFacistPoliciesEnacted = :fp, vetoPower = :vp, policiesInHand = :pih, deck = :dk, discard = :discard",
	        ExpressionAttributeValues={
	            ':lp' : currentGame['numberOfLiberalPoliciesEnacted'],
	            ':fp' : currentGame['numberOfFacistPoliciesEnacted'],
	            ':vp' : currentGame['vetoPower'],
	            ':pih' : currentGame['policiesInHand'],
	            ':dk' : currentGame['deck'],
	            ':discard' : currentGame['discard']
	})

	return returnValue

