var express = require('express');
var router = express.Router();
var bodyParser = require('body-parser')
var helper = require('../controllers/helper')

var urlencodedParser = bodyParser.urlencoded({ extended: false })


let game_c = require('../controllers/game_controller')
/* GET home page. */
router.get('/join_game', game_c.joingame_page);
router.post('/join_game', helper.validate_game_id, game_c.joingame);


router.get('/start_game', helper.get_game_details, game_c.game_board_page)
module.exports = router;
