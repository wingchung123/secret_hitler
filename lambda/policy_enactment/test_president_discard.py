import boto3
import sys
sys.path.insert(1, '/Users/wingchungchow/Documents/programming_projects/secret_hitler/lambda/')


from boto3.dynamodb.conditions import Key, Attr
from helper import *
from aws_credentials import awsAccessKey, awsSecretKey, awsRegion

from president_discard import *


dynamodb = boto3.resource('dynamodb',  aws_access_key_id=awsAccessKey, aws_secret_access_key=awsSecretKey, region_name=awsRegion)
TEST_CASES_EXISTS_IN_TABLE = False


def test_president_discard_liberal():
	gameID = 'test_president_discard_liberal'
	# setup test case scenario
	if not TEST_CASES_EXISTS_IN_TABLE:
		# test case items
		number_of_players = 5
		list_of_players = []
		gameTable = dynamodb.Table('secret-hitler-test')
		gameTablePlayers = []

		gameTestCase = create_test_game(gameID=gameID,numberOfPlayers=5,
			numberOfFacistPoliciesEnacted=3,currentPresidentID='3',
			deck=['L','F'], discard=['F','L','F','F'],policiesInHand=['F','F','L'])

		gameTable = dynamodb.Table('secret-hitler-test')
		resp = gameTable.put_item(Item=gameTestCase)


	event = {
		'game_id': gameID,
		'policies_in_hand': ['L','F'],
		'discard': 'F'

	}

	snsData = lambda_handler(event)

	currentGame = get_game_info(gameID)

	assert currentGame['discard'] == ['F','L','F','F','F']
	assert currentGame['policiesInHand'] == ['L','F']


def test_president_discard_facist():
	gameID = 'test_president_discard_facist'
	# setup test case scenario
	if not TEST_CASES_EXISTS_IN_TABLE:
		# test case items
		number_of_players = 5
		list_of_players = []
		gameTable = dynamodb.Table('secret-hitler-test')
		gameTablePlayers = []

		gameTestCase = create_test_game(gameID=gameID,numberOfPlayers=5,
			numberOfFacistPoliciesEnacted=3,currentPresidentID='3',
			deck=['L','F'], discard=['F','L','F','F'],policiesInHand=['F','L','L'])

		gameTable = dynamodb.Table('secret-hitler-test')
		resp = gameTable.put_item(Item=gameTestCase)


	event = {
		'game_id': gameID,
		'policies_in_hand': ['F','L'],
		'discard': 'L'

	}

	snsData = lambda_handler(event)

	currentGame = get_game_info(gameID)

	assert currentGame['discard'] == ['F','L','F','F','L']
	assert currentGame['policiesInHand'] == ['F','L']



