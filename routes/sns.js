// install sdk
// create router
// make change to app.js

var express = require('express');
var router = express.Router();
var request = require('request')

// var WebSocketClient = require('websocket').client;
// var client = new WebSocketClient();

const WebSocket = require('ws')


router.post('/', function(req, res, next) {
	const ws = new WebSocket('ws://localhost:5000')

//console.log(req.headers);
	headerJson = JSON.parse( JSON.stringify(req.headers) )
	// console.log(headerJson)

	bodyJson = JSON.parse(JSON.stringify(req.body))
	// 	console.log("the following is body")
	// console.log(bodyJson)

	if ( headerJson['x-amz-sns-message-type']  == 'SubscriptionConfirmation' ) {
		console.log("need to confirm subscription")
		request({url: bodyJson.SubscribeURL, method: 'GET'})
	} else {
		//parsing message
		console.log(bodyJson["Subject"])
		wsPayload = {}
		wsPayload.subject = bodyJson["Subject"]
		wsPayload.message = JSON.parse(bodyJson.Message)
		wsPayload.origin = 'sns'


		ws.on('open', function open(){
			console.log("socket is open")
			ws.send(JSON.stringify(wsPayload))
			ws.close()

		})
		ws.on('error', function error(error){
			console.log(error)
			
		})

		// // create websocket client
		// client.on('connect', function(connection) {
		// 	console.log('WebSocket Client Connected: ' + connection.socket);



		// 	connection.on('error', function(error) {
		// 		console.log("Connection Error: " + error.toString());
		// 	});
		// 	connection.on('close', function() {
		// 		console.log('Connection Closed...');
		// 	});

		// 	connection.sendUTF('This is sent from within SNS router')
		// 	connection.sendUTF(dataJson)

		// 	connection.close()

		// });

		// client.connect('ws://localhost:5000')


	}

	res.sendStatus(200);
	res.end();
});


module.exports = router;