import boto3
import sys
sys.path.insert(1, '/Users/wingchungchow/Documents/programming_projects/secret_hitler/lambda/')


from boto3.dynamodb.conditions import Key, Attr
from helper import *
from aws_credentials import awsAccessKey, awsSecretKey, awsRegion

from voting_sns import *

# NOTE: relies on Next Turn lambda; Make sure to change the function in AWS prior to running test

dynamodb = boto3.resource('dynamodb',  aws_access_key_id=awsAccessKey, aws_secret_access_key=awsSecretKey, region_name=awsRegion)
TEST_CASES_EXISTS_IN_TABLE = False # has to write to database each time otherwise tests fails

def test_vote_fails():
	votes = [{ 'vote': False } , { 'vote': False }, { 'vote': False }, { 'vote': True }, { 'vote': True }]

	assert does_vote_pass(votes) == False


def test_vote_passes():
	votes = [{ 'vote': False } , { 'vote': False }, { 'vote': True }, { 'vote': True }, { 'vote': True }]

	assert does_vote_pass(votes) == True



def test_vote_ties_fails():
	votes = [{ 'vote': False } , { 'vote': False }, { 'vote': False }, { 'vote': True }, { 'vote': True }, { 'vote': True }]

	assert does_vote_pass(votes) == False


# def test_vote_passes_db():

# 	gameID = 'test_vote_passes_db'
# 	# setup test case scenario
# 	if not TEST_CASES_EXISTS_IN_TABLE:
# 		# test case items
# 		number_of_players = 5
# 		list_of_players = []

# 		for i in range(0,number_of_players-3):

# 			playerID = i + 1
# 			playerName = "test" + str(playerID)
# 			list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=False))

# 		for i in range(number_of_players-3,number_of_players):

# 			playerID = i + 1
# 			playerName = "test" + str(playerID)
# 			list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=True))


# 		# batch writer to set up test cases
# 		playersTable = dynamodb.Table('secret-hitler-players-test')
# 		with playersTable.batch_writer() as batch:
# 			for player in list_of_players:
# 				batch.put_item(Item=player)


# 	event ={
# 		"game_id": gameID,
# 		"president_id": '1',
# 		"chancellor_id": '2'
# 	}
# 	assert lambda_function(event) == True



# def test_vote_fails_db():

# 	gameID = 'test_vote_passes_db'
# 	# setup test case scenario
# 	if not TEST_CASES_EXISTS_IN_TABLE:
# 		# test case items
# 		number_of_players = 5
# 		list_of_players = []

# 		for i in range(0,number_of_players-3):

# 			playerID = i + 1
# 			playerName = "test" + str(playerID)
# 			list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=True))

# 		for i in range(number_of_players-3,number_of_players):

# 			playerID = i + 1
# 			playerName = "test" + str(playerID)
# 			list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=False))


# 		# batch writer to set up test cases
# 		playersTable = dynamodb.Table('secret-hitler-players-test')
# 		with playersTable.batch_writer() as batch:
# 			for player in list_of_players:
# 				batch.put_item(Item=player)


# 	event ={
# 		"game_id": gameID,
# 		"president_id": '1',
# 		"chancellor_id": '2'
# 	}
# 	assert lambda_function(event) == False

def test_remove_players_votes():
	gameID = 'test_remove_players_votes'
	# setup test case scenario
	if not TEST_CASES_EXISTS_IN_TABLE:
		# test case items
		number_of_players = 5
		list_of_players = []
		gameTable = dynamodb.Table('secret-hitler-test')


		for i in range(0,number_of_players-3):

			playerID = i + 1
			playerName = "test" + str(playerID)
			if (playerID == 1):
				list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=False, role='H'))
			else:
				list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=False))

		for i in range(number_of_players-3,number_of_players):

			playerID = i + 1
			playerName = "test" + str(playerID)
			list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=True))


		# batch writer to set up test cases
		playersTable = dynamodb.Table('secret-hitler-players-test')
		with playersTable.batch_writer() as batch:
			for player in list_of_players:
				batch.put_item(Item=player)



	remove_previous_votes('secret-hitler-players-test', gameID)


	# test whether game table is updated
	player1 = get_player_info(gameID, '1')
	player2 = get_player_info(gameID, '2')
	player3 = get_player_info(gameID, '3')
	player4 = get_player_info(gameID, '4')
	player5 = get_player_info(gameID, '5')

	assert 'vote' not in player1
	assert 'vote' not in player2
	assert 'vote' not in player3
	assert 'vote' not in player4
	assert 'vote' not in player5



def test_vote_passes_check_db_update():
	gameID = 'test_vote_passes_check_db_update'
	# setup test case scenario
	if not TEST_CASES_EXISTS_IN_TABLE:
		# test case items
		number_of_players = 5
		list_of_players = []
		gameTable = dynamodb.Table('secret-hitler-test')


		for i in range(0,number_of_players-3):

			playerID = i + 1
			playerName = "test" + str(playerID)
			if (playerID == 1):
				list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=False, role='H'))
			else:
				list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=False))

		for i in range(number_of_players-3,number_of_players):

			playerID = i + 1
			playerName = "test" + str(playerID)
			list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=True))


		# batch writer to set up test cases
		playersTable = dynamodb.Table('secret-hitler-players-test')
		with playersTable.batch_writer() as batch:
			for player in list_of_players:
				batch.put_item(Item=player)

		gameTestCase = create_test_game(gameID=gameID,numberOfPlayers=5,currentPresidentID=str(1), deck=['L','F','F','L','F'])

		gameTable = dynamodb.Table('secret-hitler-test')
		resp = gameTable.put_item(Item=gameTestCase)


	event ={
		"game_id": gameID,
		"president_id": '1',
		"chancellor_id": '2'
	}
	snsData = lambda_function(event) 

	# test whether game table is updated
	currentGame = get_game_info(gameID)
	player = get_player_info(gameID, '1')

	assert 'vote' not in player
	assert currentGame['deck'] == ['L', 'F']
	assert currentGame['policiesInHand'] == ['L', 'F', 'F']
	assert currentGame['previousPresidentID'] == '1'
	assert currentGame['previousChancellorID'] == '2'
	assert snsData['gameID'] == gameID



def test_vote_passes_chancellor_not_hitler():
	gameID = 'test_vote_passes_chancellor_not_hitler'
	# setup test case scenario
	if not TEST_CASES_EXISTS_IN_TABLE:
		# test case items
		number_of_players = 5
		list_of_players = []
		gameTable = dynamodb.Table('secret-hitler-test')
		playersTable = dynamodb.Table('secret-hitler-players-test')
		gameTablePlayers = []



		for i in range(0,number_of_players-3):

			playerID = i + 1
			playerName = "test" + str(playerID)
			if (playerID == 2):
				list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=True, role='H'))
			else:
				list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=True))
			gameTablePlayers.append({"playerID":playerID, "playerName": playerName})

		for i in range(number_of_players-3,number_of_players):

			playerID = i + 1
			playerName = "test" + str(playerID)
			list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=True))
			gameTablePlayers.append({"playerID":playerID, "playerName": playerName})


		# batch writer to set up test cases
		with playersTable.batch_writer() as batch:
			for player in list_of_players:
				batch.put_item(Item=player)


		gameTestCase = create_test_game(gameID=gameID,numberOfPlayers=5,players=gameTablePlayers,
			numberOfFacistPoliciesEnacted=3,currentPresidentID='3',electionTracker=2,
			deck=['L','F','F','L','F'])

		gameTable = dynamodb.Table('secret-hitler-test')
		resp = gameTable.put_item(Item=gameTestCase)


	event = {
		'game_id': gameID,
		'chancellor_id': '4',
		'president_id': '3'

	}

	snsData = lambda_function(event)

	currentGame = get_game_info(gameID)

	player = get_player_info(gameID, '1')

	assert 'vote' not in player

	assert currentGame['currentPresidentID'] == '3'
	assert currentGame['electionTracker'] == 0
	assert currentGame['previousPresidentID'] == '3'
	assert currentGame['previousChancellorID'] == '4'
	assert currentGame['deck'] == ['L','F']
	assert currentGame['policiesInHand'] == ['L','F','F']


	assert snsData['policiesInHand'] == currentGame['policiesInHand']
	assert snsData['chancellorID'] == currentGame['previousChancellorID']
	assert snsData['vetoPower'] == currentGame['vetoPower']
	assert snsData['gameID'] == gameID
	assert snsData['presidentID'] == currentGame['currentPresidentID']



def test_vote_passes_chancellor_is_hitler():
	gameID = 'test_vote_passes_chancellor_is_hitler'
	# setup test case scenario
	if not TEST_CASES_EXISTS_IN_TABLE:
		# test case items
		number_of_players = 5
		list_of_players = []
		gameTable = dynamodb.Table('secret-hitler-test')
		gameTablePlayers = []



		for i in range(0,number_of_players-3):

			playerID = i + 1
			playerName = "test" + str(playerID)
			if (playerID == 2):
				list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=False, role='H'))
			else:
				list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=False))
			gameTablePlayers.append({"playerID":playerID, "playerName": playerName})



		for i in range(number_of_players-3,number_of_players):

			playerID = i + 1
			playerName = "test" + str(playerID)
			list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=True))
			gameTablePlayers.append({"playerID":playerID, "playerName": playerName})



		# batch writer to set up test cases
		playersTable = dynamodb.Table('secret-hitler-players-test')
		with playersTable.batch_writer() as batch:
			for player in list_of_players:
				batch.put_item(Item=player)



		gameTestCase = create_test_game(gameID=gameID,numberOfPlayers=5,
			players=gameTablePlayers, numberOfFacistPoliciesEnacted=3)

		gameTable = dynamodb.Table('secret-hitler-test')
		resp = gameTable.put_item(Item=gameTestCase)


	event ={
		"game_id": gameID,
		"president_id": '1',
		"chancellor_id": '2'
	}

	snsData = lambda_function(event)
	currentGame = get_game_info(gameID)

	assert snsData['end_game_status'] == 'F2'
	assert currentGame['endGameStatus'] == 'F2'

def test_vote_fails_new_president_to_elect():

	gameID = 'test_vote_fails_new_president_to_elect'
	# setup test case scenario
	if not TEST_CASES_EXISTS_IN_TABLE:
		# test case items
		number_of_players = 5
		list_of_players = []
		gameTable = dynamodb.Table('secret-hitler-test')
		playersTable = dynamodb.Table('secret-hitler-players-test')
		gameTablePlayers = []



		for i in range(0,number_of_players-3):

			playerID = i + 1
			playerName = "test" + str(playerID)
			if (playerID == 2):
				list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=False, role='H'))
			else:
				list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=False))
			gameTablePlayers.append({"playerID":playerID, "playerName": playerName})

		for i in range(number_of_players-3,number_of_players):

			playerID = i + 1
			playerName = "test" + str(playerID)
			list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=False))
			gameTablePlayers.append({"playerID":playerID, "playerName": playerName})


		# batch writer to set up test cases
		with playersTable.batch_writer() as batch:
			for player in list_of_players:
				batch.put_item(Item=player)


		gameTestCase = create_test_game(gameID=gameID,numberOfPlayers=5,players=gameTablePlayers,
			numberOfFacistPoliciesEnacted=3,currentPresidentID='3',electionTracker=0)

		gameTable = dynamodb.Table('secret-hitler-test')
		resp = gameTable.put_item(Item=gameTestCase)


	event = {
		'game_id': gameID,
		'chancellor_id': '4'

	}

	snsData = lambda_function(event)

	currentGame = get_game_info(gameID)

	player = get_player_info(gameID, '1')

	assert 'vote' not in player

	assert currentGame['currentPresidentID'] == '4'
	assert currentGame['electionTracker'] == 1
	assert currentGame['currentChancellorID'] == 'Null'



def test_vote_fails_election_tracker_3_top_card_liberal():
	gameID = 'test_vote_fails_election_tracker_3_top_card_liberal'
	# setup test case scenario
	if not TEST_CASES_EXISTS_IN_TABLE:
		# test case items
		number_of_players = 5
		list_of_players = []
		gameTable = dynamodb.Table('secret-hitler-test')
		playersTable = dynamodb.Table('secret-hitler-players-test')
		gameTablePlayers = []



		for i in range(0,number_of_players-3):

			playerID = i + 1
			playerName = "test" + str(playerID)
			if (playerID == 2):
				list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=False, role='H'))
			else:
				list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=False))
			gameTablePlayers.append({"playerID":playerID, "playerName": playerName})

		for i in range(number_of_players-3,number_of_players):

			playerID = i + 1
			playerName = "test" + str(playerID)
			list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=False))
			gameTablePlayers.append({"playerID":playerID, "playerName": playerName})


		# batch writer to set up test cases
		with playersTable.batch_writer() as batch:
			for player in list_of_players:
				batch.put_item(Item=player)


		gameTestCase = create_test_game(gameID=gameID,numberOfPlayers=5,players=gameTablePlayers,
			numberOfFacistPoliciesEnacted=3,numberOfLiberalPoliciesEnacted=1,
			currentPresidentID='5',electionTracker=2,deck=['L','F','F','L','F'])

		gameTable = dynamodb.Table('secret-hitler-test')
		resp = gameTable.put_item(Item=gameTestCase)


	event = {
		'game_id': gameID,
		'chancellor_id': '4'

	}

	snsData = lambda_function(event)

	currentGame = get_game_info(gameID)

	player = get_player_info(gameID, '1')

	assert 'vote' not in player

	assert currentGame['currentPresidentID'] == '1'
	assert currentGame['electionTracker'] == 0
	assert currentGame['numberOfFacistPoliciesEnacted'] == 3
	assert currentGame['numberOfLiberalPoliciesEnacted'] == 2
	assert currentGame['deck'] == ['F','F','L','F']
	assert currentGame['previousPresidentID'] == "Null"
	assert currentGame['previousChancellorID'] == "Null"
	assert currentGame['currentChancellorID'] == 'Null'




def test_vote_fails_election_tracker_3_top_card_facist():
	gameID = 'test_vote_fails_election_tracker_3_top_card_facist'
	# setup test case scenario
	if not TEST_CASES_EXISTS_IN_TABLE:
		# test case items
		number_of_players = 5
		list_of_players = []
		gameTable = dynamodb.Table('secret-hitler-test')
		playersTable = dynamodb.Table('secret-hitler-players-test')
		gameTablePlayers = []



		for i in range(0,number_of_players-3):

			playerID = i + 1
			playerName = "test" + str(playerID)
			if (playerID == 2):
				list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=False, role='H'))
			else:
				list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=False))
			gameTablePlayers.append({"playerID":playerID, "playerName": playerName})

		for i in range(number_of_players-3,number_of_players):

			playerID = i + 1
			playerName = "test" + str(playerID)
			list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=False))
			gameTablePlayers.append({"playerID":playerID, "playerName": playerName})


		# batch writer to set up test cases
		with playersTable.batch_writer() as batch:
			for player in list_of_players:
				batch.put_item(Item=player)


		gameTestCase = create_test_game(gameID=gameID,numberOfPlayers=5,players=gameTablePlayers,
			numberOfFacistPoliciesEnacted=0,numberOfLiberalPoliciesEnacted=2,
			currentPresidentID='5',electionTracker=2,deck=['F','L','L','L','L'])

		gameTable = dynamodb.Table('secret-hitler-test')
		resp = gameTable.put_item(Item=gameTestCase)


	event = {
		'game_id': gameID,
		'chancellor_id': '4'

	}

	snsData = lambda_function(event)

	currentGame = get_game_info(gameID)

	player = get_player_info(gameID, '1')

	assert 'vote' not in player

	assert currentGame['currentPresidentID'] == '1'
	assert currentGame['electionTracker'] == 0
	assert currentGame['numberOfFacistPoliciesEnacted'] == 1
	assert currentGame['numberOfLiberalPoliciesEnacted'] == 2
	assert currentGame['deck'] == ['L','L','L','L']
	assert currentGame['previousPresidentID'] == "Null"
	assert currentGame['previousChancellorID'] == "Null"
	assert currentGame['currentChancellorID'] == 'Null'



def test_vote_fails_at_3_top_policy_enables_veto_power():
	gameID = 'test_vote_fails_at_3_top_policy_enables_veto_power'
	# setup test case scenario
	if not TEST_CASES_EXISTS_IN_TABLE:
		# test case items
		number_of_players = 5
		list_of_players = []
		gameTable = dynamodb.Table('secret-hitler-test')
		playersTable = dynamodb.Table('secret-hitler-players-test')
		gameTablePlayers = []



		for i in range(0,number_of_players-3):

			playerID = i + 1
			playerName = "test" + str(playerID)
			if (playerID == 2):
				list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=False, role='H'))
			else:
				list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=False))
			gameTablePlayers.append({"playerID":playerID, "playerName": playerName})

		for i in range(number_of_players-3,number_of_players):

			playerID = i + 1
			playerName = "test" + str(playerID)
			list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=False))
			gameTablePlayers.append({"playerID":playerID, "playerName": playerName})


		# batch writer to set up test cases
		with playersTable.batch_writer() as batch:
			for player in list_of_players:
				batch.put_item(Item=player)


		gameTestCase = create_test_game(gameID=gameID,numberOfPlayers=5,players=gameTablePlayers,
			numberOfFacistPoliciesEnacted=4,numberOfLiberalPoliciesEnacted=2,
			currentPresidentID='5',electionTracker=2,deck=['F','L','L','L','L'])

		gameTable = dynamodb.Table('secret-hitler-test')
		resp = gameTable.put_item(Item=gameTestCase)


	event = {
		'game_id': gameID,
		'chancellor_id': '4'

	}

	snsData = lambda_function(event)

	currentGame = get_game_info(gameID)
	
	player = get_player_info(gameID, '1')

	assert 'vote' not in player

	assert currentGame['currentPresidentID'] == '1'
	assert currentGame['electionTracker'] == 0
	assert currentGame['numberOfFacistPoliciesEnacted'] == 5
	assert currentGame['numberOfLiberalPoliciesEnacted'] == 2
	assert currentGame['deck'] == ['L','L','L','L']
	assert currentGame['vetoPower'] == True
	assert currentGame['previousPresidentID'] == "Null"
	assert currentGame['previousChancellorID'] == "Null"
	assert currentGame['currentChancellorID'] == 'Null'

def test_vote_fails_at_3_top_policy_facists_win():
	gameID = 'test_vote_fails_at_3_top_policy_facists_win'
	# setup test case scenario
	if not TEST_CASES_EXISTS_IN_TABLE:
		# test case items
		number_of_players = 5
		list_of_players = []
		gameTable = dynamodb.Table('secret-hitler-test')
		playersTable = dynamodb.Table('secret-hitler-players-test')
		gameTablePlayers = []



		for i in range(0,number_of_players-3):

			playerID = i + 1
			playerName = "test" + str(playerID)
			if (playerID == 2):
				list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=False, role='H'))
			else:
				list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=False))
			gameTablePlayers.append({"playerID":playerID, "playerName": playerName})

		for i in range(number_of_players-3,number_of_players):

			playerID = i + 1
			playerName = "test" + str(playerID)
			list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=False))
			gameTablePlayers.append({"playerID":playerID, "playerName": playerName})


		# batch writer to set up test cases
		with playersTable.batch_writer() as batch:
			for player in list_of_players:
				batch.put_item(Item=player)


		gameTestCase = create_test_game(gameID=gameID,numberOfPlayers=5,players=gameTablePlayers,
			numberOfFacistPoliciesEnacted=5,numberOfLiberalPoliciesEnacted=2,
			currentPresidentID='5',electionTracker=2,deck=['F','L','L','L','L'],vetoPower=True)

		gameTable = dynamodb.Table('secret-hitler-test')
		resp = gameTable.put_item(Item=gameTestCase)


	event = {
		'game_id': gameID,
		'chancellor_id': '4'

	}

	snsData = lambda_function(event)

	currentGame = get_game_info(gameID)
	
	player = get_player_info(gameID, '1')

	assert 'vote' not in player

	assert currentGame['currentPresidentID'] == '1'
	assert currentGame['electionTracker'] == 0
	assert currentGame['numberOfFacistPoliciesEnacted'] == 6
	assert currentGame['numberOfLiberalPoliciesEnacted'] == 2
	assert currentGame['deck'] == ['L','L','L','L']
	assert currentGame['vetoPower'] == True
	assert currentGame['previousPresidentID'] == "Null"
	assert currentGame['previousChancellorID'] == "Null"
	assert currentGame['currentChancellorID'] == 'Null'
	assert currentGame['endGameStatus'] == 'F1'

def test_vote_fails_at_3_top_policy_liberals_win():
	gameID = 'test_vote_fails_at_3_top_policy_facists_win'
	# setup test case scenario
	if not TEST_CASES_EXISTS_IN_TABLE:
		# test case items
		number_of_players = 5
		list_of_players = []
		gameTable = dynamodb.Table('secret-hitler-test')
		playersTable = dynamodb.Table('secret-hitler-players-test')
		gameTablePlayers = []



		for i in range(0,number_of_players-3):

			playerID = i + 1
			playerName = "test" + str(playerID)
			if (playerID == 2):
				list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=False, role='H'))
			else:
				list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=False))
			gameTablePlayers.append({"playerID":playerID, "playerName": playerName})

		for i in range(number_of_players-3,number_of_players):

			playerID = i + 1
			playerName = "test" + str(playerID)
			list_of_players.append(create_test_player(playerID=str(playerID), playerName=playerName, gameID=gameID, vote=False))
			gameTablePlayers.append({"playerID":playerID, "playerName": playerName})


		# batch writer to set up test cases
		with playersTable.batch_writer() as batch:
			for player in list_of_players:
				batch.put_item(Item=player)


		gameTestCase = create_test_game(gameID=gameID,numberOfPlayers=5,players=gameTablePlayers,
			numberOfFacistPoliciesEnacted=5,numberOfLiberalPoliciesEnacted=4,
			currentPresidentID='5',electionTracker=2,deck=['L','F','L','L','L'],vetoPower=True)

		gameTable = dynamodb.Table('secret-hitler-test')
		resp = gameTable.put_item(Item=gameTestCase)


	event = {
		'game_id': gameID,
		'chancellor_id': '4'

	}

	snsData = lambda_function(event)

	currentGame = get_game_info(gameID)
	
	player = get_player_info(gameID, '1')

	assert 'vote' not in player

	assert currentGame['currentPresidentID'] == '1'
	assert currentGame['electionTracker'] == 0
	assert currentGame['numberOfFacistPoliciesEnacted'] == 5
	assert currentGame['numberOfLiberalPoliciesEnacted'] == 5
	assert currentGame['deck'] == ['F','L','L','L']
	assert currentGame['vetoPower'] == True
	assert currentGame['previousPresidentID'] == "Null"
	assert currentGame['previousChancellorID'] == "Null"
	assert currentGame['currentChancellorID'] == 'Null'
	assert currentGame['endGameStatus'] == 'L1'

# def test_vote_resets_afterwards():

# def test_veto_power_true():

# def test_write_to_db_previous_office():

# def test_vote_passes_policies_are_top_3_from_deck():

# def test_votes_are_cleared_in_db():

# def test_vote_passes_election_tracker_reset():

# def test_vote_fails_election_tracker_increments():

# def test_vote_fails_at_3_election_tracker_reset():


# moved to policy enactment lambda
# def test_shuffle_discard_deck():


























