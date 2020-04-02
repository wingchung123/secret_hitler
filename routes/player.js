var express = require('express');
var router = express.Router();
var bodyParser = require('body-parser')
var helper = require('../controllers/helper')


var urlencodedParser = bodyParser.urlencoded({ extended: false })


let player_c = require('../controllers/player_controller')
/* GET home page. */
router.get('/', helper.get_game_details, helper.get_player_details, player_c.index_page);

module.exports = router;
