var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');

const debug = false;
const local = false; // **************** NEED TO CHANGE IN PRODUCTION *****************************

var indexRouter = require('./routes/index');
// var usersRouter = require('./routes/users');
var playerRouter = require('./routes/player');
var gameRouter = require('./routes/game');
var snsRouter = require('./routes/sns');


var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');



// For unknown reasons, aws sns http/post messages will have an empty body unless you chance the content type
overrideContentType = function(){
  return function(req, res, next) {
    if (req.headers['x-amz-sns-message-type']) {
        req.headers['content-type'] = 'application/json;charset=UTF-8';
    }
    next();
  };
}
app.use(overrideContentType());

if (!local) {
	console.log("on aws server... subscribing to sns topic")
	// Subscribe to SNS topic
	const aws = require('aws-sdk');
	const request = require('request')
	const sns = new aws.SNS({ region: 'us-east-1' }); //Hardcoded value


	request({
		url: 'http://169.254.169.254/latest/meta-data/public-ipv4',
		method: 'GET',
		timeout: 5000}, function (err, resp, body) {
		console.log("getting meta-data...")
		ip_address = 'http://' + body + '/sns'
		console.log(ip_address)

		params = {
			Protocol: 'http',
			TopicArn: 'arn:aws:sns:us-east-1:271871444055:secret-hitler',
			Endpoint: ip_address
		};

		sns.subscribe(params, function(err, data) {
	        if (err) console.log(err, err.stack); // an error occurred
	                else {
						console.log("this is data:")
						console.log(data);
					}
		});
	});

}



if (debug){
	// custom middleware create
	const LoggerMiddleware = (req,res,next) =>{
	    console.log(`Logged  ${req.url}  ${req.method} -- ${new Date()}`)
	    next();
	}

	// application level middleware
	app.use(LoggerMiddleware);
}

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', indexRouter);
// app.use('/users', usersRouter);
app.use('/player', playerRouter);
app.use('/game', gameRouter);
app.use('/sns', snsRouter);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error', {errorMessage: err.message, game_id: typeof req.cookies.gameID !==  'undefined' ? req.cookies.gameID : 'Null'});
});




module.exports = app;
