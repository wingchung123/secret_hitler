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
	assert snsData['gameID'] == gameID
	assert snsData['specialElectionPresidentPlaceholder'] == 'Null'
	assert snsData['chancellorID'] == 'Null'
	
	assert game_info['currentPresidentID'] == '1'
	assert game_info['specialElectionPresidentPlaceholder'] == 'Null'
	assert game_info['currentChancellorID'] == 'Null'




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
	assert snsData['gameID'] == gameID
	assert snsData['specialElectionPresidentPlaceholder'] == 'Null'
	assert snsData['chancellorID'] == 'Null'

	assert game_info['currentPresidentID'] == '4'
	assert game_info['specialElectionPresidentPlaceholder'] == 'Null'
	assert game_info['currentChancellorID'] == 'Null'




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
	assert snsData['gameID'] == gameID
	assert snsData['specialElectionPresidentPlaceholder'] == 'Null'
	assert snsData['chancellorID'] == 'Null'

	assert game_info['currentPresidentID'] == '1'
	assert game_info['specialElectionPresidentPlaceholder'] == 'Null'
	assert game_info['currentChancellorID'] == 'Null'


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
	assert snsData['gameID'] == gameID
	assert snsData['specialElectionPresidentPlaceholder'] == 'Null'
	assert snsData['chancellorID'] == 'Null'

	assert game_info['currentPresidentID'] == '2'
	assert game_info['specialElectionPresidentPlaceholder'] == 'Null'
	assert game_info['currentChancellorID'] == 'Null'


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
	assert snsData['gameID'] == gameID
	assert snsData['chancellorID'] == 'Null'
	assert snsData['specialElectionPresidentPlaceholder'] == '5'


	assert game_info['currentPresidentID'] == '4'
	assert game_info['specialElectionPresidentPlaceholder'] == '5' # place holder for when holding special election
	assert game_info['currentChancellorID'] == 'Null'
	assert game_info['executiveAction'] == 'Null'


# Test case specifically for AFTER a special election has occurred
def test_president_exists_special_election_next_turn():
	# set up test scenario
	gameID = "test_president_exists_special_election_next_turn"

	if not TEST_CASES_EXISTS_IN_TABLE:
		players = [
			{'playerID': "1", "playerName":'test1'},
			{'playerID': "2", "playerName":'test2'},
			{'playerID': "3", "playerName":'test3'},
			{'playerID': "4", "playerName":'test4'},
			{'playerID': "5", "playerName":'test5'}

		]
		gameTestCase = create_test_game(gameID=gameID,numberOfPlayers=5,
			players=players,currentPresidentID=str(3),
			specialElectionPresidentPlaceholder=str(5))

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
	assert snsData['gameID'] == gameID
	assert snsData['chancellorID'] == 'Null'
	assert snsData['specialElectionPresidentPlaceholder'] == 'Null'


	assert game_info['currentPresidentID'] == '1'
	assert game_info['specialElectionPresidentPlaceholder'] == 'Null'
	assert game_info['currentChancellorID'] == 'Null'
	assert game_info['executiveAction'] == 'Null'



def test_president_exists_clear_chancellorID():
	# set up test scenario
	gameID = "test_president_exists_clear_chancellorID"

	if not TEST_CASES_EXISTS_IN_TABLE:
		players = [
			{'playerID': "1", "playerName":'test1'},
			{'playerID': "2", "playerName":'test2'},
			{'playerID': "3", "playerName":'test3'},
			{'playerID': "4", "playerName":'test4'},
			{'playerID': "5", "playerName":'test5'}

		]
		gameTestCase = create_test_game(gameID=gameID,numberOfPlayers=5,
			players=players,currentPresidentID=str(3),currentChancellorID=str(4),
			previousChancellorID=str(4),previousPresidentID=str(3))

		gameTable = dynamodb.Table('secret-hitler-test')
		resp = gameTable.put_item(Item=gameTestCase)

	event={
	"game_id" : gameID
	}
	snsData = lambda_function(event)

	game_info = get_game_info(gameID)


	assert snsData['presidentID'] == '4'
	assert len(snsData['listOfPlayers']) > 0
	assert snsData['previousPresidentID'] == '3'
	assert snsData['previousChancellorID'] == '4'
	assert snsData['electionTracker'] == 0
	assert snsData['gameID'] == gameID
	assert snsData['specialElectionPresidentPlaceholder'] == 'Null'
	assert snsData['chancellorID'] == 'Null'


	assert game_info['currentPresidentID'] == '4'
	assert game_info['specialElectionPresidentPlaceholder'] == 'Null'
	assert game_info['currentChancellorID'] == 'Null'


def test_president_exists_clear_executive_action_result():
	# set up test scenario
	gameID = "test_president_exists_clear_executive_action_result"

	if not TEST_CASES_EXISTS_IN_TABLE:
		players = [
			{'playerID': "1", "playerName":'test1'},
			{'playerID': "2", "playerName":'test2'},
			{'playerID': "3", "playerName":'test3'},
			{'playerID': "4", "playerName":'test4'},
			{'playerID': "5", "playerName":'test5'}

		]
		gameTestCase = create_test_game(gameID=gameID,numberOfPlayers=5,
			players=players,currentPresidentID=str(3),currentChancellorID=str(4), executiveActionResult="Not Hitler",
			previousChancellorID=str(4),previousPresidentID=str(3))

		gameTable = dynamodb.Table('secret-hitler-test')
		resp = gameTable.put_item(Item=gameTestCase)

	event={
	"game_id" : gameID
	}
	snsData = lambda_function(event)

	game_info = get_game_info(gameID)


	assert snsData['presidentID'] == '4'
	assert len(snsData['listOfPlayers']) > 0
	assert snsData['previousPresidentID'] == '3'
	assert snsData['previousChancellorID'] == '4'
	assert snsData['electionTracker'] == 0
	assert snsData['gameID'] == gameID
	assert snsData['specialElectionPresidentPlaceholder'] == 'Null'
	assert snsData['chancellorID'] == 'Null'


	assert game_info['currentPresidentID'] == '4'
	assert game_info['specialElectionPresidentPlaceholder'] == 'Null'
	assert game_info['currentChancellorID'] == 'Null'
	assert game_info['executiveActionResult'] == 'Null'
