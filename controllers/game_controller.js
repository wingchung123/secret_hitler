var request = require('request')
var cookieParser = require('cookie-parser')
var helper = require('./helper')
var net = require('net')



exports.joingame = function(req, res, next) {
	//validate whether the game id entered is valid
	if (res.locals.statusCode == 200){
		if (req.cookies.gameID == req.body.gameCode && typeof req.cookies.playerID != 'undefined'){
			// check to see if cookie has the same code as the game player is trying to join
			// player ID must not be empty
			// if so, player is joining a game they were just playing
			res.redirect('/player')
		} else {
			// they are joining a new game
			res.cookie('gameID', req.body.gameCode, { maxAge: helper.max_cookie_age})
			// joining new game so delete all previous game state cookies
			helper.delete_player_cookies(req, res)
			helper.delete_game_created_cookies(req,res)
			res.redirect('/createPlayer')
		}

	} else {
		// Error: keep on same page and request new code
		res.render('game/index', { status_code: res.locals.statusCode, game_id:'Null' });
	}
	
};


exports.joingame_page = function(req, res, next) {
	// request(api_options, callback)
	res.render('game/index', {game_id: 'Null'});
};

exports.game_board_page = function(req, res,next){
	let data = res.locals.data
	console.log(data)

	// console.log('---------------------------start socket connection---------------------------')
	// const client = net.createConnection({port: 4000}, function() {
	// 	console.log('Client: I have connected')
	// 	client.write('Client: hello this is client')
	// });

	// client.on('data', function(data){
	// 	console.log(data.toString());
	// 	client.end()
	// })

	// client.on('end', function(){
	// 	console.log('Client disconnected...')
	// })


	if (res.locals.gameDetailsStatusCode != 200){
		res.redirect("/error") //also redirects if ejs fails to render i.e. variable names don't match with input args
	} else {
		res.render('game/board', { 
			game_id: req.cookies.gameID,
			helper : helper,
			number_of_players: data.numberOfPlayers,
			number_of_liberal_policies_enacted: data.numberOfLiberalPoliciesEnacted,
			number_of_facist_policies_enacted: data.numberOfFacistPoliciesEnacted,
			list_of_players: data.players,
			list_of_executed_players : data.executedPlayers,
			previousPresidentID : data.previousPresidentID,
			previousChancellorID : data.previousChancellorID,
			presidentID : data.presidentID,
			vetoPower : data.vetoPower,
			electionTracker : data.electionTracker,
			policies_in_hand : data.policiesInHand,
			chancellorID: data.chancellorID,
			executive_action : data.executiveAction,
			playerID : data.playerID
		})
	}


};

exports.new_player_event = function(req, res, next){
	// console.log('inside add player functions')
	let data = req.body
	// console.log(data.playerName)
	res.render('game/userCard', {playerName: data.playerName, playerID: data.playerID})

}

exports.new_policies_event = function(req, res, next){
	console.log('inside policy')
	let data = req.body
	console.log(data.policiesInHand)
	res.render('game/policies', {policies_in_hand: data})

}

exports.new_policies_radio_event = function(req, res, next){
	console.log('inside policy radio')
	let data = req.body
	console.log(data.policiesInHand)
	res.render('game/policies_radio', {policies_in_hand: data})

}

exports.investigate_loyalty_select = function(req, res, next){
	console.log('inside investigate select')
	let data = req.body
	res.render('game/investigate_loyalty_select', {list_of_players: data})

}

exports.policy_enactment = function(req, res, next){
	console.log('policy enact')
	let data = req.body
	const api_options = {
		url: helper.api_url + '/policy-enactment',
		method: 'POST',
		body: data,
		headers: helper.api_key,
		json: true
	};
	request(api_options, function(err,resp,body){
		api_resp = helper.parse_api_resp(resp)
		console.log(api_resp)
		if(api_resp.statusCode == 200){
			console.log("successfully enacted policy")
		}
	})	
	// console.log(data.playerName)
	res.status(200).end()
}

exports.next_turn = function next_turn(req, res, next){
	console.log('executive action')
	let data = req.body
	const api_options = {
		url: helper.api_url + '/next-turn',
		method: 'POST',
		body: data,
		headers: helper.api_key,
		json: true
	};
	request(api_options, function(err,resp,body){
		api_resp = helper.parse_api_resp(resp)
		console.log(api_resp)
		if(api_resp.statusCode == 200){
			console.log("special election/next turn call successful")
		}
	})	
	// console.log(data.playerName)
	res.status(200).end()
}


exports.executive_action = function executive_action(req, res, next){
	console.log('executive action')
	let data = req.body
	let executive_action_resp = ""
	const api_options = {
		url: helper.api_url + '/executive-action',
		method: 'POST',
		body: data,
		headers: helper.api_key,
		json: true
	};
	request(api_options, function(err,resp,body){
		console.log(resp.body)
		executive_action_resp = resp.body
		res.send({executiveActionResult: executive_action_resp})
	})
	
}


exports.president_policy_discard = function(req, res, next){
	// console.log('inside add player functions')
	let data = req.body
	console.log(data)
	const api_options = {
		url: helper.api_url + '/president-discard',
		method: 'POST',
		body: data,
		headers: helper.api_key,
		json: true
	};
	request(api_options, function(err,resp,body){
		api_resp = helper.parse_api_resp(resp)
		console.log(api_resp)
		if(api_resp.statusCode == 200){
			console.log("successfully discarded policy")
		}
	})	
	// console.log(data.playerName)
	res.status(200).end()

}

exports.chancellor_locked_in = function(req, res, next){
	// console.log('inside add player functions')
	let data = req.body
	// console.log(data.playerName)
	const api_options = {
		url: helper.api_url + '/chancellor-select',
		method: 'POST',
		body: data,
		headers: helper.api_key,
		json: true
	};
	request(api_options, function(err,resp,body){
		api_resp = helper.parse_api_resp(resp)
		console.log(api_resp)
		if(api_resp.statusCode == 200){
			console.log("successfully locked in chancellor")
		}
	})	
	// console.log(data.playerName)
	res.status(200).end()

}

exports.voting = function(req, res, next){
	// console.log('inside add player functions')
	// must send game ID, playerID, president_id, chancellor_id and vote
	let data = req.body
	console.log(data)
	const api_options = {
		url: helper.api_url + '/voting',
		method: 'POST',
		body: data,
		headers: helper.api_key,
		json: true
	};
	request(api_options, function(err,resp,body){
		api_resp = helper.parse_api_resp(resp)
		console.log(api_resp)
		if(api_resp.statusCode == 200){
			console.log("successfully voted")
		}
	})	
	// console.log(data.playerName)
	res.status(200).end()

}

