var express = require('express');
var router = express.Router();
var bodyParser = require('body-parser')
var helper = require('../controllers/helper')

var urlencodedParser = bodyParser.urlencoded({ extended: false })


let game_c = require('../controllers/game_controller')
/* GET home page. */
router.get('/join_game', game_c.joingame_page);
router.post('/join_game', helper.validate_game_id, game_c.joingame);


router.get('/start_game', helper.get_ip_address, helper.get_game_details, helper.get_player_details, helper.get_facist_players, game_c.game_board_page)
router.get('/end_game', helper.get_game_details, helper.get_player_roles, game_c.end_game_page)
router.get('/join_audience', helper.get_game_details, game_c.join_audience)



router.post('/new_player_event', game_c.new_player_event)
router.post('/new_policies_event', game_c.new_policies_event)
router.post('/new_policies_radio_event', game_c.new_policies_radio_event)
router.post('/chancellor_locked_in', game_c.chancellor_locked_in)
router.post('/president_policy_discard', game_c.president_policy_discard)
router.post('/policy_enactment', game_c.policy_enactment)
router.post('/executive_action', game_c.executive_action)
router.post('/next_turn', game_c.next_turn)
router.post('/investigate_loyalty_select', game_c.investigate_loyalty_select)


router.post('/voting', game_c.voting)


module.exports = router;
