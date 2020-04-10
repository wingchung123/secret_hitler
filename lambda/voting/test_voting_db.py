import boto3
import sys
sys.path.insert(1, '/Users/wingchungchow/Documents/programming_projects/secret_hitler/lambda/')


from boto3.dynamodb.conditions import Key, Attr
from helper import *
from aws_credentials import awsAccessKey, awsSecretKey, awsRegion

from voting_db import *


dynamodb = boto3.resource('dynamodb',  aws_access_key_id=awsAccessKey, aws_secret_access_key=awsSecretKey, region_name=awsRegion)
TEST_CASES_EXISTS_IN_TABLE = False



def test_player_votes_no():
	# create test scenario in DB
	gameID = 'test_player_votes_no'

	if not TEST_CASES_EXISTS_IN_TABLE:
		# test case items
		number_of_players = 5
		list_of_players = []

		for i in range(0,number_of_players):

			playerID = i + 1
			playerName = "test" + str(playerID)
			list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID))

		# batch writer to set up test cases
		playersTable = dynamodb.Table('secret-hitler-players-test')
		with playersTable.batch_writer() as batch:
			for player in list_of_players:
				batch.put_item(Item=player)


	# set up parameters
	playerID = '1'
	event = {
		'game_id': gameID,
		'player_id': playerID,
		'president_id': '2',
		'chancellor_id': '3',
		'vote': False
	}

	lambda_function(event)

	playerInfo = get_player_info(gameID, playerID)

	assert playerInfo['vote'] == False 



def test_player_votes_yes():
	# create test scenario in DB
	gameID = 'test_player_votes_yes'

	if not TEST_CASES_EXISTS_IN_TABLE:
		# test case items
		number_of_players = 5
		list_of_players = []

		for i in range(0,number_of_players):

			playerID = i + 1
			playerName = "test" + str(playerID)
			list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID))

		# batch writer to set up test cases
		playersTable = dynamodb.Table('secret-hitler-players-test')
		with playersTable.batch_writer() as batch:
			for player in list_of_players:
				batch.put_item(Item=player)


	# set up parameters
	playerID = '2'
	event = {
		'game_id': gameID,
		'player_id': playerID,
		'president_id': '2',
		'chancellor_id': '3',
		'vote': True
	}

	lambda_function(event)

	playerInfo = get_player_info(gameID, playerID)

	assert playerInfo['vote'] == True 



def test_two_player_voting():

	# create test scenario in DB
	gameID = 'test_two_player_voting'

	if not TEST_CASES_EXISTS_IN_TABLE:
		# test case items
		number_of_players = 5
		list_of_players = []

		for i in range(0,number_of_players):

			playerID = i + 1
			playerName = "test" + str(playerID)
			list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID))

		# batch writer to set up test cases
		playersTable = dynamodb.Table('secret-hitler-players-test')
		with playersTable.batch_writer() as batch:
			for player in list_of_players:
				batch.put_item(Item=player)


	# set up parameters
	player1ID = '1'
	event = {
		'game_id': gameID,
		'player_id': player1ID,
		'president_id': '2',
		'chancellor_id': '3',
		'vote': False
	}

	lambda_function(event)

	player2ID = '2'
	event2 = {
		'game_id': gameID,
		'player_id': player2ID,
		'president_id': '2',
		'chancellor_id': '3',
		'vote': True
	}

	lambda_function(event2)

	player1Info = get_player_info(gameID, player1ID)
	player2Info = get_player_info(gameID, player2ID)

	assert player1Info['vote'] == False 
	assert player2Info['vote'] == True 

# unsure how to assert
# def test_invalid_president_id():


def test_players_votes_ready_true():

	gameID = 'test_players_votes_ready_true'

	if not TEST_CASES_EXISTS_IN_TABLE:
		# test case items
		number_of_players = 5
		list_of_players = []

		for i in range(0,number_of_players):

			playerID = i + 1
			playerName = "test" + str(playerID)
			list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=False))


		# batch writer to set up test cases
		playersTable = dynamodb.Table('secret-hitler-players-test')
		with playersTable.batch_writer() as batch:
			for player in list_of_players:
				batch.put_item(Item=player)


	assert checkPlayersVotesAreReady(gameID) == True


def test_players_votes_ready_false():

	gameID = 'test_players_votes_ready_false'

	if not TEST_CASES_EXISTS_IN_TABLE:
		# test case items
		number_of_players = 5
		list_of_players = []

		for i in range(0,number_of_players - 1):

			playerID = i + 1
			playerName = "test" + str(playerID)
			list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=False))

		list_of_players.append(create_test_player(playerID=str(5), playerName='test5', gameID=gameID))


		# batch writer to set up test cases
		playersTable = dynamodb.Table('secret-hitler-players-test')
		with playersTable.batch_writer() as batch:
			for player in list_of_players:
				batch.put_item(Item=player)


	assert checkPlayersVotesAreReady(gameID) == False

