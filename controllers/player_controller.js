var request = require('request')
var cookieParser = require('cookie-parser')


exports.index_page = function(req, res, next) {
	// Do NOT use cookie variables in this function
	// They are set AFTER this page is rendered therefore you will be using old values
	// playerName will be fine but to keep consistency, change to locals variable
	let data = res.locals.data

	if (res.locals.gameDetailsStatusCode != 200 || res.locals.playerDetailsStatusCode != 200){
		res.redirect(error) //also redirects if ejs fails to render i.e. variable names don't match with input args
	} else {
		res.render('player/index', { 
			player_name: data.playerName, 
			role: data.playerRole, 
			number_of_players: data.numberOfPlayers,
			number_of_liberals: data.numberOfLiberals,
			number_of_facists: data.numberOfFacists
		});
	}

};