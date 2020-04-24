import boto3
import sys
sys.path.insert(1, '/Users/wingchungchow/Documents/programming_projects/secret_hitler/lambda/')


from boto3.dynamodb.conditions import Key, Attr
from helper import *
from aws_credentials import awsAccessKey, awsSecretKey, awsRegion

from policy_enactment_db import *


dynamodb = boto3.resource('dynamodb',  aws_access_key_id=awsAccessKey, aws_secret_access_key=awsSecretKey, region_name=awsRegion)
TEST_CASES_EXISTS_IN_TABLE = False


def test_deck_shuffle_if_2_or_less():
	gameID = 'test_deck_shuffle_if_2_or_less'
	# setup test case scenario
	if not TEST_CASES_EXISTS_IN_TABLE:
		# test case items
		number_of_players = 5
		gameTable = dynamodb.Table('secret-hitler-test')
		players = [
			{'playerID': "1", "playerName":'test1'},
			{'playerID': "2", "playerName":'test2'},
			{'playerID': "3", "playerName":'test3'},
			{'playerID': "4", "playerName":'test4'},
			{'playerID': "5", "playerName":'test5'}

		]

		gameTestCase = create_test_game(gameID=gameID,numberOfPlayers=5, players=players,
			numberOfFacistPoliciesEnacted=3,currentPresidentID='3',
			deck=['L','F'], discard=['F','L','F','F'])

		gameTable = dynamodb.Table('secret-hitler-test')
		resp = gameTable.put_item(Item=gameTestCase)


	event = {
		'game_id': gameID,
		'discard': 'L',
		'enact': 'F'

	}

	snsData = lambda_function(event)

	currentGame = get_game_info(gameID)

	assert currentGame['discard'] == []
	assert currentGame['deck'][0] == 'L'
	assert currentGame['deck'][1] == 'F'
	assert currentGame['deck'].count('L') == 3
	assert currentGame['deck'].count('F') == 4
	assert len(currentGame['deck']) == 7
	assert currentGame['policiesInHand'] == []


def test_enact_liberal_policy(): # assert discard pile
	gameID = 'test_enact_liberal_policy'
	# setup test case scenario
	if not TEST_CASES_EXISTS_IN_TABLE:
		# test case items
		number_of_players = 5
		gameTable = dynamodb.Table('secret-hitler-test')
		players = [
			{'playerID': "1", "playerName":'test1'},
			{'playerID': "2", "playerName":'test2'},
			{'playerID': "3", "playerName":'test3'},
			{'playerID': "4", "playerName":'test4'},
			{'playerID': "5", "playerName":'test5'}

		]

		gameTestCase = create_test_game(gameID=gameID,numberOfPlayers=5,players=players,
			numberOfFacistPoliciesEnacted=3, numberOfLiberalPoliciesEnacted=3,currentPresidentID='3',
			deck=['L','F', 'L'], discard=['F','L','F','F'])

		gameTable = dynamodb.Table('secret-hitler-test')
		resp = gameTable.put_item(Item=gameTestCase)


	event = {
		'game_id': gameID,
		'discard': 'L',
		'enact': 'L'

	}

	snsData = lambda_function(event)

	currentGame = get_game_info(gameID)

	assert currentGame['discard'] == ['F','L','F','F','L']
	assert currentGame['deck'] == ['L','F', 'L']
	assert currentGame['numberOfFacistPoliciesEnacted'] == 3
	assert currentGame['numberOfLiberalPoliciesEnacted'] == 4
	assert currentGame['currentPresidentID'] == '4'
	assert currentGame['policiesInHand'] == []

def test_enact_liberal_policy_no_executive_action(): # assert discard pile
	gameID = 'test_enact_liberal_policy'
	# setup test case scenario
	if not TEST_CASES_EXISTS_IN_TABLE:
		# test case items
		number_of_players = 5
		gameTable = dynamodb.Table('secret-hitler-test')
		players = [
			{'playerID': "1", "playerName":'test1'},
			{'playerID': "2", "playerName":'test2'},
			{'playerID': "3", "playerName":'test3'},
			{'playerID': "4", "playerName":'test4'},
			{'playerID': "5", "playerName":'test5'}

		]

		gameTestCase = create_test_game(gameID=gameID,numberOfPlayers=5,players=players,
			numberOfFacistPoliciesEnacted=4, numberOfLiberalPoliciesEnacted=3,currentPresidentID='3',
			deck=['L','F', 'L'], discard=['F','L','F','F'])

		gameTable = dynamodb.Table('secret-hitler-test')
		resp = gameTable.put_item(Item=gameTestCase)


	event = {
		'game_id': gameID,
		'discard': 'F',
		'enact': 'L'

	}

	snsData = lambda_function(event)

	currentGame = get_game_info(gameID)

	assert currentGame['discard'] == ['F','L','F','F','F']
	assert currentGame['deck'] == ['L','F', 'L']
	assert currentGame['numberOfFacistPoliciesEnacted'] == 4
	assert currentGame['numberOfLiberalPoliciesEnacted'] == 4
	assert currentGame['executiveAction'] == 'Null'
	assert currentGame['currentPresidentID'] == '4'
	assert currentGame['policiesInHand'] == []


def test_enact_liberal_policy_end_game():
	gameID = 'test_enact_liberal_policy_end_game'
	# setup test case scenario
	if not TEST_CASES_EXISTS_IN_TABLE:
		# test case items
		number_of_players = 5
		gameTable = dynamodb.Table('secret-hitler-test')

		gameTestCase = create_test_game(gameID=gameID,numberOfPlayers=5,
			numberOfFacistPoliciesEnacted=3, numberOfLiberalPoliciesEnacted=4,currentPresidentID='3',
			deck=['L','F', 'L'], discard=['F','L','F','F'])

		gameTable = dynamodb.Table('secret-hitler-test')
		resp = gameTable.put_item(Item=gameTestCase)


	event = {
		'game_id': gameID,
		'discard': 'L',
		'enact': 'L'

	}

	returnValue = lambda_function(event)

	currentGame = get_game_info(gameID)

	assert returnValue['end_game_status'] == 'L1'
	assert currentGame['endGameStatus'] == 'L1'
	assert currentGame['discard'] == ['F','L','F','F','L']
	assert currentGame['deck'] == ['L','F', 'L']
	assert currentGame['numberOfFacistPoliciesEnacted'] == 3
	assert currentGame['numberOfLiberalPoliciesEnacted'] == 5
	assert currentGame['policiesInHand'] == []

def test_enact_facist_policy():

	gameID = 'test_enact_facist_policy'
	# setup test case scenario
	if not TEST_CASES_EXISTS_IN_TABLE:
		# test case items
		number_of_players = 5
		gameTable = dynamodb.Table('secret-hitler-test')
		players = [
			{'playerID': "1", "playerName":'test1'},
			{'playerID': "2", "playerName":'test2'},
			{'playerID': "3", "playerName":'test3'},
			{'playerID': "4", "playerName":'test4'},
			{'playerID': "5", "playerName":'test5'}

		]


		gameTestCase = create_test_game(gameID=gameID,numberOfPlayers=5,players=players,
			numberOfFacistPoliciesEnacted=1, numberOfLiberalPoliciesEnacted=3,currentPresidentID='3',
			deck=['L','F', 'L'], discard=['F','L','F','F'])

		gameTable = dynamodb.Table('secret-hitler-test')
		resp = gameTable.put_item(Item=gameTestCase)


	event = {
		'game_id': gameID,
		'discard': 'L',
		'enact': 'F'

	}

	snsData = lambda_function(event)

	currentGame = get_game_info(gameID)

	assert currentGame['discard'] == ['F','L','F','F','L']
	assert currentGame['deck'] == ['L','F', 'L']
	assert currentGame['numberOfFacistPoliciesEnacted'] == 2
	assert currentGame['numberOfLiberalPoliciesEnacted'] == 3
	assert currentGame['executiveAction'] == 'Null'
	assert currentGame['currentPresidentID'] == '4'
	assert currentGame['policiesInHand'] == []




def test_enact_facist_policy_end_game():
	gameID = 'test_enact_facist_policy_end_game'
	# setup test case scenario
	if not TEST_CASES_EXISTS_IN_TABLE:
		# test case items
		number_of_players = 5
		gameTable = dynamodb.Table('secret-hitler-test')

		gameTestCase = create_test_game(gameID=gameID,numberOfPlayers=5,
			numberOfFacistPoliciesEnacted=5, numberOfLiberalPoliciesEnacted=4,currentPresidentID='3',
			deck=['L','F', 'L'], discard=['F','L','F','F'])

		gameTable = dynamodb.Table('secret-hitler-test')
		resp = gameTable.put_item(Item=gameTestCase)


	event = {
		'game_id': gameID,
		'discard': 'L',
		'enact': 'F'

	}

	returnValue = lambda_function(event)

	currentGame = get_game_info(gameID)

	assert returnValue['end_game_status'] == 'F1'
	assert currentGame['endGameStatus'] == 'F1'
	assert currentGame['discard'] == ['F','L','F','F','L']
	assert currentGame['deck'] == ['L','F', 'L']
	assert currentGame['numberOfFacistPoliciesEnacted'] == 6
	assert currentGame['numberOfLiberalPoliciesEnacted'] == 4
	assert currentGame['policiesInHand'] == []



def test_enact_facist_policy_veto_power():
	gameID = 'test_enact_facist_policy_veto_power'
	# setup test case scenario
	if not TEST_CASES_EXISTS_IN_TABLE:
		# test case items
		number_of_players = 5
		gameTable = dynamodb.Table('secret-hitler-test')
		players = [
			{'playerID': "1", "playerName":'test1'},
			{'playerID': "2", "playerName":'test2'},
			{'playerID': "3", "playerName":'test3'},
			{'playerID': "4", "playerName":'test4'},
			{'playerID': "5", "playerName":'test5'}

		]

		gameTestCase = create_test_game(gameID=gameID,numberOfPlayers=5,players=players,
			numberOfFacistPoliciesEnacted=4, numberOfLiberalPoliciesEnacted=4,currentPresidentID='3',
			deck=['L','F', 'L'], discard=['F','L','F','F'])

		gameTable = dynamodb.Table('secret-hitler-test')
		resp = gameTable.put_item(Item=gameTestCase)


	event = {
		'game_id': gameID,
		'discard': 'L',
		'enact': 'F'

	}

	returnValue = lambda_function(event)

	currentGame = get_game_info(gameID)

	assert currentGame['discard'] == ['F','L','F','F','L']
	assert currentGame['deck'] == ['L','F', 'L']
	assert currentGame['numberOfFacistPoliciesEnacted'] == 5
	assert currentGame['numberOfLiberalPoliciesEnacted'] == 4
	assert currentGame['vetoPower'] == True
	assert currentGame['executiveAction'] == 'execution'
	assert currentGame['currentPresidentID'] == '3'
	assert currentGame['policiesInHand'] == []




def test_enact_facist_policy_party_investigation():
	gameID = 'test_enact_facist_policy_party_investigation'
	# setup test case scenario
	if not TEST_CASES_EXISTS_IN_TABLE:
		# test case items
		number_of_players = 9
		gameTable = dynamodb.Table('secret-hitler-test')

		gameTestCase = create_test_game(gameID=gameID,numberOfPlayers=number_of_players,
			numberOfFacistPoliciesEnacted=0, numberOfLiberalPoliciesEnacted=4,currentPresidentID='3',
			deck=['L','F', 'L'], discard=['F','L','F','F'])

		gameTable = dynamodb.Table('secret-hitler-test')
		resp = gameTable.put_item(Item=gameTestCase)


	event = {
		'game_id': gameID,
		'discard': 'L',
		'enact': 'F'

	}

	returnValue = lambda_function(event)

	currentGame = get_game_info(gameID)

	assert currentGame['discard'] == ['F','L','F','F','L']
	assert currentGame['deck'] == ['L','F', 'L']
	assert currentGame['numberOfFacistPoliciesEnacted'] == 1
	assert currentGame['numberOfLiberalPoliciesEnacted'] == 4
	assert currentGame['vetoPower'] == False
	assert returnValue['payload']['executiveAction'] == 'investigate_loyalty'
	assert currentGame['executiveAction'] == 'investigate_loyalty'
	assert currentGame['currentPresidentID'] == '3'
	assert currentGame['policiesInHand'] == []



def test_enact_facist_policy_policy_peek():
	gameID = 'test_enact_facist_policy_party_investigation'
	# setup test case scenario
	if not TEST_CASES_EXISTS_IN_TABLE:
		# test case items
		number_of_players = 5
		gameTable = dynamodb.Table('secret-hitler-test')

		gameTestCase = create_test_game(gameID=gameID,numberOfPlayers=number_of_players,
			numberOfFacistPoliciesEnacted=2, numberOfLiberalPoliciesEnacted=4,currentPresidentID='3',
			deck=['L','F', 'L'], discard=['F','L','F','F'])

		gameTable = dynamodb.Table('secret-hitler-test')
		resp = gameTable.put_item(Item=gameTestCase)


	event = {
		'game_id': gameID,
		'discard': 'L',
		'enact': 'F'

	}

	returnValue = lambda_function(event)

	currentGame = get_game_info(gameID)

	assert currentGame['discard'] == ['F','L','F','F','L']
	assert currentGame['deck'] == ['L','F', 'L']
	assert currentGame['numberOfFacistPoliciesEnacted'] == 3
	assert currentGame['numberOfLiberalPoliciesEnacted'] == 4
	assert currentGame['vetoPower'] == False
	assert returnValue['payload']['executiveAction'] == 'policy_peek'
	assert currentGame['executiveAction'] == 'policy_peek'
	assert currentGame['currentPresidentID'] == '3'
	assert currentGame['policiesInHand'] == []


def test_enact_facist_policy_player_execution():
	gameID = 'test_enact_facist_policy_player_execution'
	# setup test case scenario
	if not TEST_CASES_EXISTS_IN_TABLE:
		# test case items
		number_of_players = 7
		list_of_players = []
		gameTable = dynamodb.Table('secret-hitler-test')
		gameTablePlayers = []

		gameTestCase = create_test_game(gameID=gameID,numberOfPlayers=number_of_players,
			numberOfFacistPoliciesEnacted=3, numberOfLiberalPoliciesEnacted=4,currentPresidentID='3',
			deck=['L','F', 'L'], discard=['F','L','F','F'])

		gameTable = dynamodb.Table('secret-hitler-test')
		resp = gameTable.put_item(Item=gameTestCase)


	event = {
		'game_id': gameID,
		'discard': 'L',
		'enact': 'F'

	}

	returnValue = lambda_function(event)

	currentGame = get_game_info(gameID)

	assert currentGame['discard'] == ['F','L','F','F','L']
	assert currentGame['deck'] == ['L','F', 'L']
	assert currentGame['numberOfFacistPoliciesEnacted'] == 4
	assert currentGame['numberOfLiberalPoliciesEnacted'] == 4
	assert currentGame['vetoPower'] == False
	assert returnValue['payload']['executiveAction'] == 'execution'
	assert currentGame['executiveAction'] == 'execution'
	assert currentGame['currentPresidentID'] == '3'
	assert currentGame['policiesInHand'] == []



# def test_enact_facist_policy_player_execution_veto_power():
# 	gameID = 'test_enact_facist_policy_player_execution_veto_power'
# 	# setup test case scenario
# 	if not TEST_CASES_EXISTS_IN_TABLE:
# 		# test case items
# 		number_of_players = 7
# 		list_of_players = []
# 		gameTable = dynamodb.Table('secret-hitler-test')
# 		gameTablePlayers = []

# 		gameTestCase = create_test_game(gameID=gameID,numberOfPlayers=number_of_players,
# 			numberOfFacistPoliciesEnacted=4, numberOfLiberalPoliciesEnacted=4,currentPresidentID='3',
# 			deck=['L','F', 'L'], discard=['F','L','F','F'])

# 		gameTable = dynamodb.Table('secret-hitler-test')
# 		resp = gameTable.put_item(Item=gameTestCase)


# 	event = {
# 		'game_id': gameID,
# 		'discard': 'L,F',
# 		'enact': 'F'

# 	}

# 	returnValue = lambda_function(event)

# 	currentGame = get_game_info(gameID)

# 	assert currentGame['discard'] == ['F','L','F','F','L', 'F']
# 	assert currentGame['deck'] == ['L','F', 'L']
# 	assert currentGame['numberOfFacistPoliciesEnacted'] == 5
# 	assert currentGame['numberOfLiberalPoliciesEnacted'] == 4
# 	assert currentGame['vetoPower'] == True
# 	assert returnValue == 'execution'


def test_enact_facist_policy_special_election():
	gameID = 'test_enact_facist_policy_special_election'
	# setup test case scenario
	if not TEST_CASES_EXISTS_IN_TABLE:
		# test case items
		number_of_players = 7
		gameTable = dynamodb.Table('secret-hitler-test')

		gameTestCase = create_test_game(gameID=gameID,numberOfPlayers=number_of_players,
			numberOfFacistPoliciesEnacted=2, numberOfLiberalPoliciesEnacted=4,currentPresidentID='3',
			deck=['L','F', 'L'], discard=['F','L','F','F'])

		gameTable = dynamodb.Table('secret-hitler-test')
		resp = gameTable.put_item(Item=gameTestCase)


	event = {
		'game_id': gameID,
		'discard': 'L',
		'enact': 'F'

	}

	returnValue = lambda_function(event)

	currentGame = get_game_info(gameID)

	assert currentGame['discard'] == ['F','L','F','F','L']
	assert currentGame['deck'] == ['L','F', 'L']
	assert currentGame['numberOfFacistPoliciesEnacted'] == 3
	assert currentGame['numberOfLiberalPoliciesEnacted'] == 4
	assert currentGame['vetoPower'] == False
	assert returnValue['payload']['executiveAction'] == 'special_election'
	assert currentGame['executiveAction'] == 'special_election'
	assert currentGame['currentPresidentID'] == '3'
	assert currentGame['policiesInHand'] == []

	

def test_enact_veto_power():
	gameID = 'test_enact_facist_policy_special_election'
	# setup test case scenario
	if not TEST_CASES_EXISTS_IN_TABLE:
		# test case items
		number_of_players = 7
		gameTable = dynamodb.Table('secret-hitler-test')
		players = [
			{'playerID': "1", "playerName":'test1'},
			{'playerID': "2", "playerName":'test2'},
			{'playerID': "3", "playerName":'test3'},
			{'playerID': "4", "playerName":'test4'},
			{'playerID': "5", "playerName":'test5'}

		]

		gameTestCase = create_test_game(gameID=gameID,numberOfPlayers=number_of_players,policiesInHand=['F','L'],players=players,
			numberOfFacistPoliciesEnacted=5, numberOfLiberalPoliciesEnacted=4,currentPresidentID='3',
			deck=['L','F', 'L'], discard=['F','L','F','F'])

		gameTable = dynamodb.Table('secret-hitler-test')
		resp = gameTable.put_item(Item=gameTestCase)


	event = {
		'game_id': gameID,
		'discard': ['L','F'],
		'enact': 'Null'

	}

	returnValue = lambda_function(event)

	currentGame = get_game_info(gameID)

	assert currentGame['discard'] == ['F','L','F','F','F', 'L']
	assert currentGame['deck'] == ['L','F', 'L']
	assert currentGame['numberOfFacistPoliciesEnacted'] == 5
	assert currentGame['numberOfLiberalPoliciesEnacted'] == 4
	assert currentGame['vetoPower'] == True
	assert currentGame['executiveAction'] == 'Null'
	assert currentGame['currentPresidentID'] == '4'
	assert currentGame['policiesInHand'] == []


