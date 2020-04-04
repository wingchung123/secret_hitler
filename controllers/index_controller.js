var request = require('request')
var cookieParser = require('cookie-parser')
var helper = require('./helper')


exports.index_page = function(req, res, next) {
	res.render('index');
};

exports.create_player_page = function(req, res, next) {
	res.render('createPlayer')
};

/* @inputs req.body = number of players
 * @output
 
 */
exports.create_game = function(req, res, next){
	const api_options = {
		url: helper.api_url + '/game',
		method: 'POST',
		body: {"num_of_players": req.body.numPlayers},
		headers: helper.api_key,
		json: true
	};
	request(api_options, function(err,resp,body){
		api_resp = helper.parse_api_resp(resp)
		console.log(api_resp)
		if(api_resp.statusCode == 200){
			res.cookie('gameID', api_resp.data.game_id, { maxAge: helper.max_cookie_age})
			res.clearCookie('playerName')
			res.redirect('createPlayer')
		} else {
			//Shouldn't happen except for server error
			res.render('index', { status_code: api_resp.statusCode })
		}
	})	
}


exports.create_player = function(req, res, next){
	const api_options = {
		url: helper.api_url + '/player',
		method: 'POST',
		body: {"player_name": req.body.playerName, "game_id": req.cookies.gameID },
		headers: helper.api_key,
		json: true
	};
	request(api_options, function(err,resp,body){
		api_resp = helper.parse_api_resp(resp)
		console.log(api_resp)
		if(api_resp.statusCode == 200){
			res.cookie('playerName', req.body.playerName, { maxAge: helper.max_cookie_age})
			res.cookie('playerID', api_resp.data.player_id, { maxAge: helper.max_cookie_age})
			res.redirect('/player/')
		} else {
			res.render('createPlayer', {status_code: api_resp.statusCode})
		}


	})

}