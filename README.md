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

`docker run -p 49160:3000 --name test-env -d wing/secret-hitler ` run image on container; -d to run in background, -p to publish port & link to machine port

`docker ps || docker container ls`

`docker stop <container-name>`

`docker system prune`




## Useful node commands

`npm start`

`npm install <package-name> --save` (replace --save with --save-dev for dev packages)

Nodemon has been installed for dev. Code changes automatically applied




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


