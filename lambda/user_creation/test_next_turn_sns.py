import boto3
import sys
sys.path.insert(1, '/Users/wingchungchow/Documents/programming_projects/secret_hitler/lambda/')


from boto3.dynamodb.conditions import Key, Attr
from helper import *
from aws_credentials import awsAccessKey, awsSecretKey, awsRegion

from next_turn_sns import *


dynamodb = boto3.resource('dynamodb',  aws_access_key_id=awsAccessKey, aws_secret_access_key=awsSecretKey, region_name=awsRegion)
TEST_CASES_EXISTS_IN_TABLE = False


def test_no_president_exists():

	# set up test scenario
	gameID = "test_no_president_exists"

	if not TEST_CASES_EXISTS_IN_TABLE:
		players = [
			{'playerID': "1", "playerName":'test1'},
			{'playerID': "2", "playerName":'test2'},
			{'playerID': "3", "playerName":'test3'},
			{'playerID': "4", "playerName":'test4'},
			{'playerID': "5", "playerName":'test5'}

		]
		gameTestCase = create_test_game(gameID=gameID,numberOfPlayers=5,
			players=players)

		gameTable = dynamodb.Table('secret-hitler-test')
		resp = gameTable.put_item(Item=gameTestCase)


	event={
	"game_id" : gameID
	}
	snsData = lambda_function(event)

	# test dynamodb was updated
	game_info = get_game_info(gameID)


	assert snsData['presidentID'] == '1'
	assert len(snsData['listOfPlayers']) > 0
	assert snsData['previousPresidentID'] == 'Null'
	assert snsData['previousChancellorID'] == 'Null'
	assert snsData['electionTracker'] == 0
	assert game_info['currentPresidentID'] == '1'



def test_president_exists():
	# set up test scenario
	gameID = "test_president_exists"

	if not TEST_CASES_EXISTS_IN_TABLE:
		players = [
			{'playerID': "1", "playerName":'test1'},
			{'playerID': "2", "playerName":'test2'},
			{'playerID': "3", "playerName":'test3'},
			{'playerID': "4", "playerName":'test4'},
			{'playerID': "5", "playerName":'test5'}

		]
		gameTestCase = create_test_game(gameID=gameID,numberOfPlayers=5,
			players=players,currentPresidentID=str(3))

		gameTable = dynamodb.Table('secret-hitler-test')
		resp = gameTable.put_item(Item=gameTestCase)

	event={
	"game_id" : gameID
	}
	snsData = lambda_function(event)

	game_info = get_game_info(gameID)


	assert snsData['presidentID'] == '4'
	assert len(snsData['listOfPlayers']) > 0
	assert snsData['previousPresidentID'] == 'Null'
	assert snsData['previousChancellorID'] == 'Null'
	assert snsData['electionTracker'] == 0
	assert game_info['currentPresidentID'] == '4'



def test_president_exists_last_player():
	# set up test scenario
	gameID = "test_president_exists_last_player"

	if not TEST_CASES_EXISTS_IN_TABLE:
		players = [
			{'playerID': "1", "playerName":'test1'},
			{'playerID': "2", "playerName":'test2'},
			{'playerID': "3", "playerName":'test3'},
			{'playerID': "4", "playerName":'test4'},
			{'playerID': "5", "playerName":'test5'}

		]
		gameTestCase = create_test_game(gameID=gameID,numberOfPlayers=5,
			players=players,currentPresidentID=str(5))

		gameTable = dynamodb.Table('secret-hitler-test')
		resp = gameTable.put_item(Item=gameTestCase)

	event={
	"game_id" : gameID
	}
	snsData = lambda_function(event)

	game_info = get_game_info(gameID)


	assert snsData['presidentID'] == '1'
	assert len(snsData['listOfPlayers']) > 0
	assert snsData['previousPresidentID'] == 'Null'
	assert snsData['previousChancellorID'] == 'Null'
	assert snsData['electionTracker'] == 0
	assert game_info['currentPresidentID'] == '1'




def test_president_exists_w_executed_players():
	# set up test scenario
	gameID = "test_president_exists_w_executed_players"

	if not TEST_CASES_EXISTS_IN_TABLE:
		players = [
			# {'playerID': "1", "playerName":'test1'},
			{'playerID': "2", "playerName":'test2'},
			{'playerID': "3", "playerName":'test3'},
			{'playerID': "4", "playerName":'test4'},
			{'playerID': "5", "playerName":'test5'}

		]
		gameTestCase = create_test_game(gameID=gameID,numberOfPlayers=5,
			players=players,currentPresidentID=str(5))

		gameTable = dynamodb.Table('secret-hitler-test')
		resp = gameTable.put_item(Item=gameTestCase)

	event={
	"game_id" : gameID
	}
	snsData = lambda_function(event)

	game_info = get_game_info(gameID)

	assert snsData['presidentID'] == '2'
	assert len(snsData['listOfPlayers']) > 0
	assert snsData['previousPresidentID'] == 'Null'
	assert snsData['previousChancellorID'] == 'Null'
	assert snsData['electionTracker'] == 0
	assert game_info['currentPresidentID'] == '2'


def test_president_exists_special_election():
	# set up test scenario
	gameID = "test_president_exists_special_election"

	if not TEST_CASES_EXISTS_IN_TABLE:
		players = [
			{'playerID': "1", "playerName":'test1'},
			{'playerID': "2", "playerName":'test2'},
			{'playerID': "3", "playerName":'test3'},
			{'playerID': "4", "playerName":'test4'},
			{'playerID': "5", "playerName":'test5'}

		]
		gameTestCase = create_test_game(gameID=gameID,numberOfPlayers=5,
			players=players,currentPresidentID=str(5))

		gameTable = dynamodb.Table('secret-hitler-test')
		resp = gameTable.put_item(Item=gameTestCase)

	event={
	"game_id" : gameID,
	"president_id": "4"
	}
	snsData = lambda_function(event)

	game_info = get_game_info(gameID)


	assert snsData['presidentID'] == '4'
	assert len(snsData['listOfPlayers']) > 0
	assert snsData['previousPresidentID'] == 'Null'
	assert snsData['previousChancellorID'] == 'Null'
	assert snsData['electionTracker'] == 0
	assert game_info['currentPresidentID'] == '5' # special election doesn't affect original order






