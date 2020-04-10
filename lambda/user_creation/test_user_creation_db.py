# Needed for testing
import boto3
import sys
sys.path.insert(1, '/Users/wingchungchow/Documents/programming_projects/secret_hitler/lambda/')


from boto3.dynamodb.conditions import Key, Attr
from helper import *
from aws_credentials import awsAccessKey, awsSecretKey, awsRegion

# Pull in test method(s)
from user_creation_db import *



dynamodb = boto3.resource('dynamodb',  aws_access_key_id=awsAccessKey, aws_secret_access_key=awsSecretKey, region_name=awsRegion)
TEST_CASES_EXISTS_IN_TABLE = False


def test_players_ready_true():

	gameID = 'players_ready_test_true'

	if ( not TEST_CASES_EXISTS_IN_TABLE):
		# test case items
		number_of_players = 5
		list_of_players = []
		gameID = 'players_ready_test_true'

		for i in range(0,number_of_players):

			playerID = i + 1
			playerName = "test" + str(playerID)
			list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID))


		# batch writer to set up test cases
		playersTable = dynamodb.Table('secret-hitler-players-test')
		with playersTable.batch_writer() as batch:
			for player in list_of_players:
				batch.put_item(Item=player)


	assert checkPlayersAreReady(gameID) == True

def test_players_are_not_ready():

	gameID = 'players_ready_test_false'

	if ( not TEST_CASES_EXISTS_IN_TABLE):
		# test case items
		number_of_players = 6
		list_of_players = []
		gameID = 'players_ready_test_false'

		for i in range(0,number_of_players - 1):

			playerID = i + 1
			playerName = "test" + str(playerID)
			list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID))

		list_of_players.append(create_test_player(playerID=str(number_of_players), gameID=gameID, isNull=True))

		# batch writer to set up test cases
		playersTable = dynamodb.Table('secret-hitler-players-test')
		with playersTable.batch_writer() as batch:
			for player in list_of_players:
				batch.put_item(Item=player)

	assert checkPlayersAreReady(str(gameID)) == False

