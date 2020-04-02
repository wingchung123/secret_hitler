var request = require('request')

const api_url = 'https://f6rfiijh83.execute-api.us-east-1.amazonaws.com/dev'
const api_key = {'x-api-key': 'lNB8qsKchF6sNPfucZDKy7z9kLeMfeOoaXch6MxY'}
const max_cookie_age = 3600000 * 4

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
			res.cookie('numberOfPlayers', api_resp.data.numberOfPlayers, { maxAge: max_cookie_age})
			// res.cookie('numberOfFacistPolicies', api_resp.data.numberOfFacistPolicies, { maxAge: max_cookie_age})
			// res.cookie('numberOfLiberalPolicies', api_resp.data.numberOfLiberalPolicies, { maxAge: max_cookie_age})
			// res.cookie('numberOfFacists', api_resp.data.numberOfFacists, { maxAge: max_cookie_age})
			// res.cookie('numberOfLiberals', api_resp.data.numberOfLiberals, { maxAge: max_cookie_age})
			// res.cookie('numberOfLiberalPoliciesEnacted', api_resp.data.numberOfLiberalPoliciesEnacted, { maxAge: max_cookie_age})
			// res.cookie('numberOfFacistPoliciesEnacted', api_resp.data.numberOfFacistPoliciesEnacted, { maxAge: max_cookie_age})
			// res.cookie('listOfPlayers', api_resp.data.players, { maxAge: max_cookie_age})
		} else {
			// console.log(resp)
		}
		res.locals.gameDetailsStatusCode = api_resp.statusCode
		res.locals.data = {}
		res.locals.data.numberOfPlayers = api_resp.data.numberOfPlayers
		res.locals.data.numberOfFacistPolicies = api_resp.data.numberOfFacistPolicies
		res.locals.data.numberOfLiberalPolicies = api_resp.data.numberOfLiberalPolicies
		// res.locals.data.numberOfFacists = api_resp.data.numberOfFacists
		// res.locals.data.numberOfLiberals = api_resp.data.numberOfLiberals
		res.locals.data.numberOfLiberalPoliciesEnacted = api_resp.data.numberOfLiberalPoliciesEnacted
		res.locals.data.numberOfFacistPoliciesEnacted = api_resp.data.numberOfFacistPoliciesEnacted
		res.locals.data.players = api_resp.data.players

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
			// res.cookie('playerID', api_resp.data.playerID, { maxAge: max_cookie_age}) //should be set already
			// res.cookie('player_name', api_resp.data.player_name, { maxAge: max_cookie_age}) // should be set already
			// res.cookie('gameID', api_resp.data.numberOfFacists, { maxAge: max_cookie_age}) // should already have
			// res.cookie('isNull', api_resp.data.numberOfLiberals, { maxAge: max_cookie_age}) // not needed
			res.cookie('role', parse_roles_policies(api_resp.data.role), { maxAge: max_cookie_age})

		} else {
			console.log(err)

		}
		console.log(req.cookies)
		res.locals.playerDetailsStatusCode = api_resp.statusCode
		res.locals.data.playerRole = parse_roles_policies(api_resp.data.role)
		res.locals.data.playerName = api_resp.data.playerName

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