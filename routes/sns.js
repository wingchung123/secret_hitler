// install sdk
// create router
// make change to app.js

var express = require('express');
var router = express.Router();
var request = require('request')



router.post('/', function(req, res, next) {

//console.log(req.headers);
	headerJson = JSON.parse( JSON.stringify(req.headers) )
	console.log(headerJson)

	console.log("the following is body")
	bodyJson = JSON.parse(JSON.stringify(req.body))
	console.log(bodyJson)

	if ( headerJson['x-amz-sns-message-type']  == 'SubscriptionConfirmation' ) {
		console.log("need to confirm subscription")
		request({url: bodyJson.SubscribeURL, method: 'GET'})
	} else {
		//parsing message
		console.log(bodyJson["Subject"])
		switch (bodyJson.Subject) {

		case "Testing":
			console.log("This is testing");
			dataJson = JSON.parse(bodyJson.Message)
			console.log(dataJson)
			console.log(typeof dataJson)
			console.log(dataJson.data)
			break;
		case "Testing2":
			console.log("This is testing2");
			break;
		}
	}

	res.sendStatus(200);
	res.end();
});


module.exports = router;