import boto3
from boto3.dynamodb.conditions import Key, Attr

import sys
sys.path.insert(1, '/Users/wingchungchow/Documents/programming_projects/secret_hitler/lambda/')
from aws_credentials import awsAccessKey, awsSecretKey, awsRegion




dynamodb = boto3.resource('dynamodb',  aws_access_key_id=awsAccessKey, aws_secret_access_key=awsSecretKey, region_name=awsRegion)


def checkPlayersAreReady(gameID):
	gameID = str(gameID)
	table = dynamodb.Table('secret-hitler-players-test')
	resp = table.query(
		FilterExpression=Attr('isNull').eq(True),
		KeyConditionExpression=Key('gameID').eq(gameID),
		ProjectionExpression="playerID"
	);
	players_without_names = resp["Items"]

	while 'LastEvaluatedKey' in resp:
		resp = table.query(
			FilterExpression=Attr('isNull').eq(True),
			ProjectionExpression="playerID", Limit=10,
			KeyConditionExpression=Key('gameID').eq(gameID),
			ExclusiveStartKey=resp['LastEvaluatedKey'])
		players_without_names.extend(resp['Items'])

	return players_without_names == []

# print(checkPlayersAreReady(str(2)))