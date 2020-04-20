import boto3
import sys
sys.path.insert(1, '/Users/wingchungchow/Documents/programming_projects/secret_hitler/lambda/')


from boto3.dynamodb.conditions import Key, Attr
from helper import *
from aws_credentials import awsAccessKey, awsSecretKey, awsRegion

from executive_action_db import *


dynamodb = boto3.resource('dynamodb',  aws_access_key_id=awsAccessKey, aws_secret_access_key=awsSecretKey, region_name=awsRegion)
TEST_CASES_EXISTS_IN_TABLE = False


def test_policy_peek():
	gameID = 'test_policy_peek'
	# setup test case scenario
	if not TEST_CASES_EXISTS_IN_TABLE:
		# test case items
		number_of_players = 5
		gameTable = dynamodb.Table('secret-hitler-test')

		gameTestCase = create_test_game(gameID=gameID,numberOfPlayers=number_of_players,
			numberOfFacistPoliciesEnacted=3,currentPresidentID='3',electionTracker=2,
			deck=['L','F','F','L','F'])

		gameTable = dynamodb.Table('secret-hitler-test')
		resp = gameTable.put_item(Item=gameTestCase)


	event = {
		'executive_action': 'policy_peek',
		'game_id' : gameID
	}

	returnData = lambda_function(event)

	currentGame = get_game_info(gameID)

	assert currentGame['deck'] == ['L','F','F','L','F']

	assert returnData == ['L','F','F']



def test_investigate_loyalty_facist():
	gameID = 'test_investigate_loyalty_facist'
	# setup test case scenario
	if not TEST_CASES_EXISTS_IN_TABLE:
		# test case items
		number_of_players = 5
		gameTable = dynamodb.Table('secret-hitler-test')
		playersTable = dynamodb.Table('secret-hitler-players-test')
		gameTablePlayers = []
		list_of_players = []



		for i in range(0,number_of_players-3):

			playerID = i + 1
			playerName = "test" + str(playerID)
			if (playerID == 2):
				list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=True, role='H'))
			else:
				list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=True, role='F'))
			gameTablePlayers.append({"playerID":playerID, "playerName": playerName})

		for i in range(number_of_players-3,number_of_players):

			playerID = i + 1
			playerName = "test" + str(playerID)
			list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=True, role='L'))
			gameTablePlayers.append({"playerID":playerID, "playerName": playerName})


		# batch writer to set up test cases
		with playersTable.batch_writer() as batch:
			for player in list_of_players:
				batch.put_item(Item=player)


		gameTestCase = create_test_game(gameID=gameID,numberOfPlayers=number_of_players,players=gameTablePlayers,
			numberOfFacistPoliciesEnacted=3,currentPresidentID='3',electionTracker=2,
			deck=['L','F','F','L','F'])

		gameTable = dynamodb.Table('secret-hitler-test')
		resp = gameTable.put_item(Item=gameTestCase)


	event = {
		'executive_action': 'investigate_loyalty',
		'game_id' : gameID,
		'player_id' : '1'
	}

	returnData = lambda_function(event)


	assert returnData == 'Facist'


def test_investigate_loyalty_liberal():
	gameID = 'test_investigate_loyalty_liberal'
	# setup test case scenario
	if not TEST_CASES_EXISTS_IN_TABLE:
		# test case items
		number_of_players = 5
		gameTable = dynamodb.Table('secret-hitler-test')
		playersTable = dynamodb.Table('secret-hitler-players-test')
		gameTablePlayers = []
		list_of_players = []



		for i in range(0,number_of_players-3):

			playerID = i + 1
			playerName = "test" + str(playerID)
			if (playerID == 2):
				list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=True, role='H'))
			else:
				list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=True, role='F'))
			gameTablePlayers.append({"playerID":playerID, "playerName": playerName})

		for i in range(number_of_players-3,number_of_players):

			playerID = i + 1
			playerName = "test" + str(playerID)
			list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=True, role='L'))
			gameTablePlayers.append({"playerID":playerID, "playerName": playerName})


		# batch writer to set up test cases
		with playersTable.batch_writer() as batch:
			for player in list_of_players:
				batch.put_item(Item=player)


		gameTestCase = create_test_game(gameID=gameID,numberOfPlayers=number_of_players,players=gameTablePlayers,
			numberOfFacistPoliciesEnacted=3,currentPresidentID='3',electionTracker=2,
			deck=['L','F','F','L','F'])

		gameTable = dynamodb.Table('secret-hitler-test')
		resp = gameTable.put_item(Item=gameTestCase)


	event = {
		'executive_action': 'investigate_loyalty',
		'game_id' : gameID,
		'player_id' : '5'
	}

	returnData = lambda_function(event)


	assert returnData == 'Liberal'


def test_investigate_loyalty_hitler_return_facist():
	gameID = 'test_investigate_loyalty_hitler_return_facist'
	# setup test case scenario
	if not TEST_CASES_EXISTS_IN_TABLE:
		# test case items
		number_of_players = 5
		gameTable = dynamodb.Table('secret-hitler-test')
		playersTable = dynamodb.Table('secret-hitler-players-test')
		gameTablePlayers = []
		list_of_players = []



		for i in range(0,number_of_players-3):

			playerID = i + 1
			playerName = "test" + str(playerID)
			if (playerID == 2):
				list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=True, role='H'))
			else:
				list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=True, role='F'))
			gameTablePlayers.append({"playerID":playerID, "playerName": playerName})

		for i in range(number_of_players-3,number_of_players):

			playerID = i + 1
			playerName = "test" + str(playerID)
			list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=True, role='L'))
			gameTablePlayers.append({"playerID":playerID, "playerName": playerName})


		# batch writer to set up test cases
		with playersTable.batch_writer() as batch:
			for player in list_of_players:
				batch.put_item(Item=player)


		gameTestCase = create_test_game(gameID=gameID,numberOfPlayers=number_of_players,players=gameTablePlayers,
			numberOfFacistPoliciesEnacted=3,currentPresidentID='3',electionTracker=2,
			deck=['L','F','F','L','F'])

		gameTable = dynamodb.Table('secret-hitler-test')
		resp = gameTable.put_item(Item=gameTestCase)


	event = {
		'executive_action': 'investigate_loyalty',
		'game_id' : gameID,
		'player_id' : '2'
	}

	returnData = lambda_function(event)

	assert returnData == 'Facist'



def test_execution_hitler():
	gameID = 'test_execution_hitler'
	# setup test case scenario
	if not TEST_CASES_EXISTS_IN_TABLE:
		# test case items
		number_of_players = 5
		gameTable = dynamodb.Table('secret-hitler-test')
		playersTable = dynamodb.Table('secret-hitler-players-test')
		gameTablePlayers = []
		list_of_players = []



		for i in range(0,number_of_players-3):

			playerID = i + 1
			playerName = "test" + str(playerID)
			if (playerID == 2):
				list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=True, role='H'))
			else:
				list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=True, role='F'))
			gameTablePlayers.append({"playerID":playerID, "playerName": playerName})

		for i in range(number_of_players-3,number_of_players):

			playerID = i + 1
			playerName = "test" + str(playerID)
			list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=True, role='L'))
			gameTablePlayers.append({"playerID":playerID, "playerName": playerName})


		# batch writer to set up test cases
		with playersTable.batch_writer() as batch:
			for player in list_of_players:
				batch.put_item(Item=player)


		gameTestCase = create_test_game(gameID=gameID,numberOfPlayers=number_of_players,players=gameTablePlayers,
			numberOfFacistPoliciesEnacted=3,currentPresidentID='3',electionTracker=2,
			deck=['L','F','F','L','F'])

		gameTable = dynamodb.Table('secret-hitler-test')
		resp = gameTable.put_item(Item=gameTestCase)


	event = {
		'executive_action': 'execution',
		'game_id' : gameID,
		'player_id' : '2'
	}

	returnData = lambda_function(event)


	assert returnData == 'Liberals Win; Hitler is killed.'


def test_execution_not_hitler():
	gameID = 'test_execution_hitler'
	# setup test case scenario
	if not TEST_CASES_EXISTS_IN_TABLE:
		# test case items
		number_of_players = 5
		gameTable = dynamodb.Table('secret-hitler-test')
		playersTable = dynamodb.Table('secret-hitler-players-test')
		gameTablePlayers = []
		list_of_players = []



		for i in range(0,number_of_players-3):

			playerID = i + 1
			playerName = "test" + str(playerID)
			if (playerID == 2):
				list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=True, role='H'))
			else:
				list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=True, role='F'))
			gameTablePlayers.append({"playerID":playerID, "playerName": playerName})

		for i in range(number_of_players-3,number_of_players):

			playerID = i + 1
			playerName = "test" + str(playerID)
			list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=True, role='L'))
			gameTablePlayers.append({"playerID":playerID, "playerName": playerName})


		# batch writer to set up test cases
		with playersTable.batch_writer() as batch:
			for player in list_of_players:
				batch.put_item(Item=player)


		gameTestCase = create_test_game(gameID=gameID,numberOfPlayers=number_of_players,players=gameTablePlayers,
			numberOfFacistPoliciesEnacted=3,currentPresidentID='3',electionTracker=2,
			deck=['L','F','F','L','F'])

		gameTable = dynamodb.Table('secret-hitler-test')
		resp = gameTable.put_item(Item=gameTestCase)


	event = {
		'executive_action': 'execution',
		'game_id' : gameID,
		'player_id' : '1'
	}

	returnData = lambda_function(event)

	currentGame = get_game_info(gameID)
	playerInfo = get_player_info(gameID, '1')

	for player in currentGame['players']:
		assert player['playerID'] != '1'

	currentGame['executedPlayers'][0]['playerID'] == '1'

	assert playerInfo['isAlive'] == False





# def test_vote_passes_chancellor_not_hitler():
# 	gameID = 'test_vote_passes_chancellor_not_hitler'
# 	# setup test case scenario
# 	if not TEST_CASES_EXISTS_IN_TABLE:
# 		# test case items
# 		number_of_players = 5
# 		list_of_players = []
# 		gameTable = dynamodb.Table('secret-hitler-test')
# 		playersTable = dynamodb.Table('secret-hitler-players-test')
# 		gameTablePlayers = []



# 		for i in range(0,number_of_players-3):

# 			playerID = i + 1
# 			playerName = "test" + str(playerID)
# 			if (playerID == 2):
# 				list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=True, role='H'))
# 			else:
# 				list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=True))
# 			gameTablePlayers.append({"playerID":playerID, "playerName": playerName})

# 		for i in range(number_of_players-3,number_of_players):

# 			playerID = i + 1
# 			playerName = "test" + str(playerID)
# 			list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=True))
# 			gameTablePlayers.append({"playerID":playerID, "playerName": playerName})


# 		# batch writer to set up test cases
# 		with playersTable.batch_writer() as batch:
# 			for player in list_of_players:
# 				batch.put_item(Item=player)


# 		gameTestCase = create_test_game(gameID=gameID,numberOfPlayers=5,players=gameTablePlayers,
# 			numberOfFacistPoliciesEnacted=3,currentPresidentID='3',electionTracker=2,
# 			deck=['L','F','F','L','F'])

# 		gameTable = dynamodb.Table('secret-hitler-test')
# 		resp = gameTable.put_item(Item=gameTestCase)


# 	event = {
# 		'game_id': gameID,
# 		'chancellor_id': '4',
# 		'president_id': '3'

# 	}

# 	snsData = lambda_function(event)

# 	currentGame = get_game_info(gameID)

# 	player = get_player_info(gameID, '1')

# 	assert 'vote' not in player

# 	assert currentGame['currentPresidentID'] == '3'
# 	assert currentGame['electionTracker'] == 0
# 	assert currentGame['previousPresidentID'] == '3'
# 	assert currentGame['previousChancellorID'] == '4'
# 	assert currentGame['deck'] == ['L','F']
# 	assert currentGame['policiesInHand'] == ['L','F','F']


# 	assert snsData['policiesInHand'] == currentGame['policiesInHand']
# 	assert snsData['chancellorID'] == currentGame['previousChancellorID']
# 	assert snsData['vetoPower'] == currentGame['vetoPower']

