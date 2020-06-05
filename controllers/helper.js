var request = require('request')

const api_url = 'https://f6rfiijh83.execute-api.us-east-1.amazonaws.com/dev'
const api_key = {'x-api-key': 'lNB8qsKchF6sNPfucZDKy7z9kLeMfeOoaXch6MxY'}
const max_cookie_age = 3600000 * 4
const list_of_cookies = ['numberOfPlayers', 'presidentID', 'chancellorID',
 'previousChancellorID', 'previousPresidentID', 'policiesInHand', 'executiveAction', 'executiveActionResult',
 'numberOfFacistPoliciesEnacted', 'numberOfLiberalPoliciesEnacted',
 'numberOfLiberalPolicies', 'numberOfFacistPolicies', 'vetoPower', 'fpids', 'hpid'] //also all the playerIDs // exclued chancellorID

const list_of_player_cookies = ['playerID', 'playerName', 'role']

// const list_of_game_created_cookies = ['chancellorID', 'locked_in', 'policiesInHand', 'executiveAction']

exports.api_url = api_url
exports.api_key = api_key
exports.max_cookie_age = max_cookie_age



function parse_roles_policies(text){
	returnValue = ""
	switch (text){
		case "L":
			returnValue = "Liberal"
			break;
		case "F":
			returnValue = "Facist"
			break;
		case "H":
			returnValue = "Hitler"
			break;
	}
	return returnValue
}

function parse_api_resp(res){
	if (res.statusCode == "418") {
		error = res.body.errorMessage
		errorCode = error.substring(error.indexOf("[") + 1, error.length - 1)
		console.log("Error Code: " + errorCode)
		returnValue = {
			"statusCode" : errorCode,
			"message" : error,
			"data": null
		}
	} else if (res.statusCode == "400") {
		returnValue = {
			"error" : res.body.errorMessage,
			"response" : res
		}
	} else if (res.statusCode == "200") {
		returnValue = {
			"statusCode" : res.statusCode,
			"message" : res.body.message,
			"data": res.body.data
		}
	} else {
		returnValue = {
			"statusCode" : res.statusCode,
			"message": res.body.message,
			"data" : null
		}
	}
	return returnValue
}

exports.parse_api_resp = parse_api_resp
exports.parse_roles_policies = parse_roles_policies

exports.delete_player_cookies = function delete_player_cookies(req, res){

	list_of_player_cookies.forEach(function(item,index){
		res.clearCookie(item)
	})
}

exports.delete_game_state_cookies = function delete_game_state_cookies(req, res){

	let numberOfPlayers = req.cookies.numberOfPlayers
	for (let i = 1; i <= numberOfPlayers; i++){
		res.clearCookie(i)
		res.clearCookie('ghost'+i)
	}

	list_of_cookies.forEach(function(item,index){
		res.clearCookie(item)
	})
}

// exports.delete_game_created_cookies = function delete_game_created_cookies(req, res){

// 	list_of_game_created_cookies.forEach(function(item,index){
// 		res.clearCookie(item)
// 	})
// }

exports.validate_game_id = function validate_game_id(req, res, next){
	const api_options = {
		url: api_url + '/game/details?table=game&game_id=' + req.body.gameCode,
		method: 'GET',
		headers: api_key,
		json: true
	};
	request(api_options, function(err,resp,body){
		// console.log(resp)
		api_resp = parse_api_resp(resp)
		console.log(api_resp)
		res.locals.statusCode = api_resp.statusCode
		next()
	})
}

exports.get_ip_address = function validate_game_id(req, res, next){
	request({
		url: 'http://169.254.169.254/latest/meta-data/public-ipv4',
		method: 'GET',
		timeout: 1500}, function (err, resp, body) {
		console.log("getting meta-data...")
		ip_address =  body
		console.log(ip_address)
		res.locals.ip_address = typeof ip_address == 'undefined' ? '192.168.99.100' : ip_address // 192.168.99.100 - local docker // localhost:3000

		next()
	});
}


exports.get_game_details = function get_game_details(req, res, next){
	console.log("inside helper.get_game_details...")

	const api_options = {
		url: api_url + '/game/details?table=game&game_id=' + req.cookies.gameID,
		method: 'GET',
		headers: api_key,
		json: true
	};
	request(api_options, function(err,resp,body){
		// console.log(resp)
		api_resp = parse_api_resp(resp)
		console.log(api_resp)
		if(api_resp.statusCode == 200){
			// these values will not be ready until AFTER the page renders
			// clear player cookies before resetting
			for(var i = 1; i <= api_resp.data.numberOfPlayers; i++){
				res.clearCookie(i)
			}
			exports.delete_game_state_cookies(req,res)


			res.cookie('numberOfPlayers', api_resp.data.numberOfPlayers, { maxAge: max_cookie_age})
			// res.cookie('numberOfFacistPolicies', api_resp.data.numberOfFacistPolicies, { maxAge: max_cookie_age})
			// res.cookie('numberOfLiberalPolicies', api_resp.data.numberOfLiberalPolicies, { maxAge: max_cookie_age})
			// res.cookie('numberOfFacists', api_resp.data.numberOfFacists, { maxAge: max_cookie_age})
			// res.cookie('numberOfLiberals', api_resp.data.numberOfLiberals, { maxAge: max_cookie_age})
			res.cookie('numberOfLiberalPoliciesEnacted', api_resp.data.numberOfLiberalPoliciesEnacted, { maxAge: max_cookie_age})
			res.cookie('numberOfFacistPoliciesEnacted', api_resp.data.numberOfFacistPoliciesEnacted, { maxAge: max_cookie_age})
			res.cookie('vetoPower', api_resp.data.vetoPower, { maxAge: max_cookie_age})
			res.cookie('previousPresidentID', api_resp.data.previousPresidentID, { maxAge: max_cookie_age, path:'/'})
			res.cookie('previousChancellorID', api_resp.data.previousChancellorID, { maxAge: max_cookie_age})
			res.cookie('presidentID', api_resp.data.currentPresidentID, { maxAge: max_cookie_age})
			res.cookie('electionTracker', api_resp.data.electionTracker, { maxAge: max_cookie_age})
			res.cookie('chancellorID', api_resp.data.currentChancellorID, { maxAge: max_cookie_age})
			res.cookie('executiveAction', api_resp.data.executiveAction, { maxAge: max_cookie_age})
			if (api_resp.data.currentPresidentID.toString() == req.cookies.playerID.toString() ){
				console.log(decodeURIComponent(api_resp.data.executiveActionResult))
				res.cookie('executiveActionResult', decodeURIComponent(api_resp.data.executiveActionResult), { maxAge: max_cookie_age})
			}
			if (api_resp.data.policiesInHand.length > 0) {

				if ( (api_resp.data.currentPresidentID.toString() == req.cookies.playerID.toString() && api_resp.data.policiesInHand.length == 3) ||
						(api_resp.data.currentChancellorID.toString() == req.cookies.playerID.toString() && api_resp.data.policiesInHand.length == 2) ){
					console.log('President or chancellors turn to discard policies')
					res.cookie('policiesInHand', api_resp.data.policiesInHand.toString().replace(/,/g,'p'), { maxAge: max_cookie_age})
				} else {
					res.cookie('policiesInHand', api_resp.data.policiesInHand.length, { maxAge: max_cookie_age})
				}
			} else {
				console.log('policies null')
				res.cookie('policiesInHand', 'Null', { maxAge: max_cookie_age})
			}


			api_resp.data.players.forEach(function(item, index){
				res.cookie(item.playerID, item.playerName, { maxAge: max_cookie_age})
			})

			api_resp.data.executedPlayers.forEach(function(item,index){
				res.cookie('ghost'+item.playerID, item.playerName, { maxAge: max_cookie_age})
			})
		} else {
			res.locals.message = api_resp.message
		}
		try{
			res.locals.gameDetailsStatusCode = api_resp.statusCode
			res.locals.data = {}
			res.locals.data.numberOfPlayers = api_resp.data.numberOfPlayers
			res.locals.data.numberOfFacistPolicies = api_resp.data.numberOfFacistPolicies
			res.locals.data.numberOfLiberalPolicies = api_resp.data.numberOfLiberalPolicies
			res.locals.data.numberOfFacists = api_resp.data.numberOfFacists //used in player.index.ejs
			res.locals.data.numberOfLiberals = api_resp.data.numberOfLiberals //used in player.index.ejs
			res.locals.data.numberOfLiberalPoliciesEnacted = api_resp.data.numberOfLiberalPoliciesEnacted
			res.locals.data.numberOfFacistPoliciesEnacted = api_resp.data.numberOfFacistPoliciesEnacted
			res.locals.data.players = api_resp.data.players
			res.locals.data.executedPlayers = api_resp.data.executedPlayers
			res.locals.data.previousPresidentID = api_resp.data.previousPresidentID
			res.locals.data.previousChancellorID = api_resp.data.previousChancellorID
			res.locals.data.presidentID = api_resp.data.currentPresidentID
			res.locals.data.chancellorID = api_resp.data.currentChancellorID
			res.locals.data.vetoPower = api_resp.data.vetoPower
			res.locals.data.electionTracker = api_resp.data.electionTracker
			res.locals.data.policiesInHand = api_resp.data.policiesInHand
			res.locals.data.executiveAction = api_resp.data.executiveAction
			res.locals.data.playerID = req.cookies.playerID,
			res.locals.data.endGame = api_resp.data.endGameStatus

		} catch (e) {
			res.locals.gameDetailsError = e
		}


		next()

	})

}

// requires get_game_details to be called first
exports.get_player_details = function get_player_details(req, res, next){
	console.log("inside helper.get_player_details...")
	const api_options = {
		url: api_url + '/game/details?table=player&game_id=' + req.cookies.gameID + '&player_id=' + req.cookies.playerID,
		method: 'GET',
		headers: api_key,
		json: true
	};
	request(api_options, function(err,resp,body){
		// console.log(resp)
		api_resp = parse_api_resp(resp)
		console.log(api_resp)
		if(api_resp.statusCode == 200){
			res.cookie('playerID', api_resp.data.playerID, { maxAge: max_cookie_age}) //should be set already
			res.cookie('playerName', api_resp.data.playerName, { maxAge: max_cookie_age}) // should be set already //set again for force join
			// res.cookie('gameID', api_resp.data.gameID, { maxAge: max_cookie_age}) // should already have
			// res.cookie('isNull', api_resp.data.isNull, { maxAge: max_cookie_age}) // not needed
			res.cookie('role', parse_roles_policies(api_resp.data.role), { maxAge: max_cookie_age})

		} else {
			res.locals.message = api_resp.message
		}
		try {
			res.locals.playerDetailsStatusCode = api_resp.statusCode
			res.locals.data.playerRole = parse_roles_policies(api_resp.data.role)
			res.locals.data.playerName = api_resp.data.playerName
		} catch (e) {
			res.locals.playerDetailsError = e
		}


		next()
	})	

}

// requires get_game_details to be called first
exports.get_facist_players = function get_facist_players(req, res, next){
	console.log("inside helper.get_facist_players...")
	const api_options = {
		url: api_url + '/facist-players?game_id=' + req.cookies.gameID,
		method: 'GET',
		headers: api_key,
		json: true
	};
	request(api_options, function(err,resp,body){
		// console.log(resp)
		api_resp = parse_api_resp(resp)
		console.log(api_resp)
		if (res.locals.data.playerRole == 'Facist' || (res.locals.data.playerRole == 'Hitler' && res.locals.data.numberOfPlayers < 7) ){
			if(api_resp.statusCode == 200){
			// res.cookie('playerID', api_resp.data.playerID, { maxAge: max_cookie_age}) //should be set already
			// res.cookie('playerName', api_resp.data.playerName, { maxAge: max_cookie_age}) // should be set already //set again for force join
			// // res.cookie('gameID', api_resp.data.gameID, { maxAge: max_cookie_age}) // should already have
			// // res.cookie('isNull', api_resp.data.isNull, { maxAge: max_cookie_age}) // not needed
			// res.cookie('role', parse_roles_policies(api_resp.data.role), { maxAge: max_cookie_age})
			let fpids = ''
			api_resp.data.forEach(function(item, index){
				if (item.role == 'H') {
					res.cookie('hpid', item.playerID, { maxAge: max_cookie_age})
				} else {
					fpids += item.playerID + 'F'
				}
			})
			res.cookie('fpids', fpids, { maxAge: max_cookie_age})

			} else {
				res.locals.message = api_resp.message
			}
			try {
				// console.log(res.locals.data.playerRole)
				// console.log(res.locals.data.playerRole == 'F')
				// console.log(res.locals.data.playerRole == 'Hitler')
				// console.log(res.locals.data.numberOfPlayers < 7)
				// console.log((res.locals.data.playerRole == 'H' && res.locals.data.numberOfPlayers < 7) )
				// console.log((res.locals.data.playerRole == 'Facist' || (res.locals.data.playerRole == 'Hitler' && res.locals.data.numberOfPlayers < 7) ))
				res.locals.data.facistPlayers = api_resp.data
				
			} catch (e) {
				res.locals.playerDetailsError = e
			}

		}



		next()
	})	

}

// requires get_game_details to be called first
exports.get_player_roles = function (req, res, next){
	console.log("inside helper.get_player_roles...")
	const api_options = {
		url: api_url + '/player?game_id=' + req.cookies.gameID,
		method: 'GET',
		headers: api_key,
		json: true
	};
	request(api_options, function(err,resp,body){
		// console.log(resp)
		api_resp = parse_api_resp(resp)
		console.log(api_resp)
		if(api_resp.statusCode == 200){
		// res.cookie('playerID', api_resp.data.playerID, { maxAge: max_cookie_age}) //should be set already
		// res.cookie('playerName', api_resp.data.playerName, { maxAge: max_cookie_age}) // should be set already //set again for force join
		// // res.cookie('gameID', api_resp.data.gameID, { maxAge: max_cookie_age}) // should already have
		// // res.cookie('isNull', api_resp.data.isNull, { maxAge: max_cookie_age}) // not needed
		// res.cookie('role', parse_roles_policies(api_resp.data.role), { maxAge: max_cookie_age})
		} else {
			res.locals.message = api_resp.message
		}
		try {
			let liberalPlayers = []
			let facistPlayers = []
			let hitler = {}

			api_resp.data.forEach(function(item,index){
				item.role = parse_roles_policies(item.role)
				if (item.role == 'Hitler') {
					hitler = item
				} else if (item.role == 'Facist') {
					facistPlayers.push(item)
				} else if (item.role == 'Liberal') {
					liberalPlayers.push(item)
				}
			})

			res.locals.data.liberalPlayers = liberalPlayers
			res.locals.data.facistPlayers = facistPlayers
			res.locals.data.hitler = hitler
			
		} catch (e) {
			res.locals.playerDetailsError = e
		}

	

		next()
	})	

}


exports.get_image_url = function get_image_url(numOfPlayers, isFacistBoard, numOfPoliciesEnacted) {

	image_url_value = ""
	if (isFacistBoard){
		if (numOfPlayers < 7 ) {
			switch (numOfPoliciesEnacted) {
				case 0:
					image_url_value = '/images/boards/small/facist_board_5_6.png';
					break;
				case 1:
					image_url_value = '/images/boards/small/facist_board_5_6_1.png';
					break;
				case 2:
					image_url_value = '/images/boards/small/facist_board_5_6_2.png';
					break;
				case 3:
					image_url_value = '/images/boards/small/facist_board_5_6_3.png';
					break;
				case 4:
					image_url_value = '/images/boards/small/facist_board_5_6_4.png';
					break;
				case 5:
					image_url_value = '/images/boards/small/facist_board_5_6_5.png';
					break;
				case 6:
					image_url_value = '/images/boards/small/facist_board_5_6_6.png';
					break;
				default:
					image_url_value = 'error in switch statement'
					break;
			}
		} else if (numOfPlayers < 9) {
			switch (numOfPoliciesEnacted) {
				case 0:
					image_url_value = '/images/boards/medium/facist_board_7_8.png'
					break;
				case 1:
					image_url_value = '/images/boards/medium/facist_board_7_8_1.png'
					break;
				case 2:
					image_url_value = '/images/boards/medium/facist_board_7_8_2.png'
					break;
				case 3:
					image_url_value = '/images/boards/medium/facist_board_7_8_3.png'
					break;
				case 4:
					image_url_value = '/images/boards/medium/facist_board_7_8_4.png'
					break;
				case 5:
					image_url_value = '/images/boards/medium/facist_board_7_8_5.png'
					break;
				case 6:
					image_url_value = '/images/boards/medium/facist_board_7_8_6.png'
					break;
				default:
					image_url_value = 'error in switch statement'
					break;
			}

		} else if (numOfPlayers < 11) {
			switch (numOfPoliciesEnacted) {
				case 0:
					image_url_value = '/images/boards/large/facist_board_9_10.png'
					break;
				case 1:
					image_url_value = '/images/boards/large/facist_board_9_10_1.png'
					break;
				case 2:
					image_url_value = '/images/boards/large/facist_board_9_10_2.png'
					break;
				case 3:
					image_url_value = '/images/boards/large/facist_board_9_10_3.png'
					break;
				case 4:
					image_url_value = '/images/boards/large/facist_board_9_10_4.png'
					break;
				case 5:
					image_url_value = '/images/boards/large/facist_board_9_10_5.png'
					break;
				case 6:
					image_url_value = '/images/boards/large/facist_board_9_10_6.png'
					break;
				default:
					image_url_value = 'error in switch statement'
					break;
			}

		} else {
			//error
			console.log("Invalid number of players")
			image_url_value = 'Invalid number of players'
		}
	} else {
		switch (numOfPoliciesEnacted) {
			case 0:
				image_url_value = '/images/boards/liberal/liberal_board.png'
				break;
			case 1:
				image_url_value = '/images/boards/liberal/liberal_board_1.png'
				break;
			case 2:
				image_url_value = '/images/boards/liberal/liberal_board_2.png'
				break;
			case 3:
				image_url_value = '/images/boards/liberal/liberal_board_3.png'
				break;
			case 4:
				image_url_value = '/images/boards/liberal/liberal_board_4.png'
				break;
			case 5:
				image_url_value = '/images/boards/liberal/liberal_board_5.png'
				break;
			default:
				image_url_value = 'error in switch statement'
				break;
		}
	}
	return image_url_value
}