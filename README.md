# Secret Hitler Game

Uses containers, express & AWS resources (back-end)

Game Rules: https://secrethitler.com/assets/Secret_Hitler_Rules.pdf

[Markdown Guide](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)

Sublime Markdown -> Markdown Preview Package, alt-m to preview

Sample Pictures: https://medium.com/@mackenzieschubert/secret-hitler-illustration-graphic-design-435be3e3586c

(policy: 188px by 268px)

Web sockets: https://www.pubnub.com/blog/nodejs-websocket-programming-examples/

Web sockets broadcasting: https://medium.com/factory-mind/websocket-node-js-express-step-by-step-using-typescript-725114ad5fe4

Nodejs & SNS topic error (an error that wasted 2hrs of my life): https://stackoverflow.com/questions/18484775/how-do-you-access-an-amazon-sns-post-body-with-express-node-js

Dynamodb Python Examples: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html

Dynamodb Docs: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/dynamodb.html#boto3.dynamodb.conditions.Attr


## Useful docker commands 
[Docker Guide](https://nodejs.org/en/docs/guides/nodejs-docker-webapp/)

`eval $(docker-machine env default)` to configure terminal shell

`docker-machine ip default` show docker-machine ip

`docker build -t wing/secret-hitler .` build image

`docker run -p 49160:3000 -p 5000:5000 --name test-env -d wing/secret-hitler ` run image on container; -d to run in background, -p to publish port & link to machine port

`docker ps || docker container ls`

`docker stop <container-name>`

`docker system prune`

`docker exec -it <container-name/id> /bin/bash` log into the docker container via bash terminal




## Useful node commands

`npm start`

`npm install <package-name> --save` (replace --save with --save-dev for dev packages)

Nodemon has been installed for dev. Code changes automatically applied



## Deployment

1. Test Locally

2. Build docker image and test in local docker machine (make changes to Dockerfile if applicable)

3. Run AWS Code Build to create new docker image in AWS ECR

4. Spin up EC2 for ECS service (via ASG)

5. Test via public IPv4 address

6. Debug by logging into the ec2 instance, looking up the docker container info and logging into it

7. You'll need to install vim to edit files (apt-update, apt-get install vim)

8. You need to kill the existing node-server (ps -e|grep node, kill -9 XXX )




## Nodejs Web Dev Tutorials

[Nodejs Response Object](https://www.tutorialspoint.com/nodejs/nodejs_response_object.htm)

[Using cookies](https://www.tutorialspoint.com/expressjs/expressjs_cookies.htm)

[Bootstrap Typography](https://www.w3schools.com/bootstrap/bootstrap_typography.asp)



## Future Enhancements


| Function        | Use Case           | Sudo-code  |
| --------------- |--------------------| -----------|
| Force Player Login| When a user wants to rejoin a game (via cookie) but they enter the incorrect game ID so it overwrites the original cookie gameID| Add a button on player create the opens a new dialogue. First check to see if name exists for that game id, if it does, have the function return player id, log it in the cookie and proceed to player index |
| Region agnostic| Currently, the region is all defaulted to us-east-1 in AWS infrastructure as well as app.js SNS subscription | not sure|
| if you reload at any point, you will lose most game data? Especially if President||
| make sure to check every SNS/Peer message has a gameID otherwise everyone will get notified||




## Test Cases

| Test Scenario   | Test Inputs        | Expected Outputs   | Resources affected |
| --------------- |--------------------| -------------------|--------------------|






## DynamoDB Test Cases


| Test Scenario   | Table    | Unique ID       | Test Case |
| --------------- |----------| --------------- |-----------|
| All players are created | secret-hitler-players | gameID = 1 | lambda user_creation|



## Cookie Management


|  Cookie Name  | Function Set | Used for | Source |
| ------------- |--------------| -------- | ------ |
| playerID | index_controller.create_player | identifying player| client input
| gameID | index_controller.create_game | identifying game| client input
| numberOfPlayers | helper.get_game_details | counting TOTAL players | DynamoDB.secret-hitler
| \{playerID\}=\{playerName\}| helper.get_game_details OR websocket.snsParseEvent | deconstructed list of players | DynamoDB.secret-hitler OR sns notification
| playerName | helper.get_player_details OR index_controller.create_player | player display name | DynamoDB.player OR client input
| role | helper.get_player_details | player role| DynamoDB.secret-hitler-players
| presidentID | websocket.peerParseEvent | selected presidentID | peer notification
| chancellorID | websocket.peerParseEvent | selected chancellorID | peer notification
| previousPresidentID | websocket.snsParseEvent | previous president ID | sns notification
| previousChancellorID | websocket.snsParseEvent | previous chancellor ID | sns notification




## Game States

Next Turn -> Lock In Chancellor

Lock In Chancellor -> Voting (Fails; Election tracker + 1)

Lock In Chancellor -> Voting (Fails; Election tracker = 0; Enact top policy)

Lock In Chancellor -> Voting (Pass)

Voting (Fails; Election tracker + 1) -> Next Turn

Voting (Fails; Election tracker = 0; Enact top policy) -> Next Turn

Voting (Fails; Election tracker = 0; Enact top policy) -> End Game

Voting (Pass) -> End Game

Voting (Pass) -> President Discard

President Discard -> Policy Enactment

Policy Enactment -> Next Turn

Policy Enactment -> Executive Action

Executive Action -> End Game

Executive Action -> Next Turn




- Next Turn:
	DB State:
	1. Chancellor ID = Null
	2. Executive Action = Null OR Special Election
	3. President ID = new president id OR special election president id
	4. special election presdient placeholder = placeholder ID or null
	5. Previous president ID
	6. Previous chancellor ID
	7. Number of Facist/Liberal policies
	8. Veto Power
	9. Executive Action Result = Null

	Web State:
	1. Pop up for president to select chancellor
	2. Enable & show (or disable & hide) chancellor selection
	3. no executive action display (except for special election)
	4. Disable voting/hide voting if executed
	5. Update election tracker
	6. update game boards
	7. enable veto power


- Lock In Chancellor:
	1. Chancellor ID != Null

	1. Disable chancellor selection
	2. Enable voting


- Voting (processing votes):
	1. Policies in hand = deck[0:3]
	2. Deck.length >= 3
	3. Election tracker
	4. Votes != 'Null'::before

	1. Embed/Delete Policies
	2. Show/Hide policy accordion
	3. Disable voting


	OR

	1. Next turn lambda execution

	1. Disable voting


- President Discard
	1. Votes == Null
	2. Policies in hand.length == 2
	3. Discard + 1

	1. Pass cards on to Chancellor

- Chancellor Discard/policy enactment
	1. Deck.length >= 3 (shuffle)
	2. Discard + 1
	3. Number of liberal policies/facist policies + 1
	4. Veto Power
	5. Policies in Hand = []


- Executive Action
	1. Executive Action = Null
	2. Executive Action Result != Null


Web Reload States:
- If Chancellor ID is null, election time?
- If executive action is not null, then executive action?
- What happens if you submit executive action -> game['executiveAction'] is now null -> on client, instead of clicking okay you refresh the page?



