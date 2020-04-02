var request = require('request')
var cookieParser = require('cookie-parser')
var helper= require('./helper')



exports.joingame = function(req, res, next) {
	//validate whether the game id entered is valid
	if (res.locals.statusCode == 200){
		if (req.cookies.gameID == req.body.gameCode && typeof req.cookies.playerName != 'undefined'){
			// check to see if cookie has the same code as the game player is trying to join
			// player name must not be empty
			// if so, player is joining a game they were just playing
			res.redirect('/player')
		} else {
			// they are joining a new game
			res.cookie('gameID', req.body.gameCode, { maxAge: helper.max_cookie_age})
			res.redirect('/createPlayer')
		}

	} else {
		// Error: keep on same page and request new code
		res.render('game/index', { status_code: res.locals.statusCode });
	}
	
};


exports.joingame_page = function(req, res, next) {
	// request(api_options, callback)
	res.render('game/index');
};

exports.game_board_page = function(req, res,next){
	let data = res.locals.data
	console.log(data)
	if (res.locals.gameDetailsStatusCode != 200){
		res.redirect(error) //also redirects if ejs fails to render i.e. variable names don't match with input args
	} else {
		res.render('game/board', { 
			helper : helper,
			number_of_players: data.numberOfPlayers,
			number_of_liberal_policies_enacted: data.numberOfLiberalPoliciesEnacted,
			number_of_facist_policies_enacted: data.numberOfFacistPoliciesEnacted,
			list_of_players: data.players
		})
	}


};

