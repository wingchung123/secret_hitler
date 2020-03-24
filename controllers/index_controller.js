var request = require('request')

const options = {
	url: 'https://bf93648mb6.execute-api.us-east-1.amazonaws.com/test',
	method: 'POST',
	body: {"num_of_players":"5"},
	headers: {
		'x-api-key': 'lNB8qsKchF6sNPfucZDKy7z9kLeMfeOoaXch6MxY'
	},

	json: true
};

function callback(err, res, body){
	console.log("Status code: " + res.statusCode)
	console.log(body)

}
exports.index = function(req, res, next) {
	request(options, callback)
	res.render('index', { title: 'Testing' });
};

