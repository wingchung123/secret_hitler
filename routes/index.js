var express = require('express');
var router = express.Router();
var bodyParser = require('body-parser')

var urlencodedParser = bodyParser.urlencoded({ extended: false })


let index_c = require('../controllers/index_controller')
/* GET home page. */
router.get('/', index_c.index_page);
router.get('/gameRules', index_c.game_rules);
router.post('/createGame', urlencodedParser, index_c.create_game)


router.get('/createPlayer', index_c.create_player_page);
router.post('/createPlayer', urlencodedParser, index_c.create_player)

router.post('/forceJoin', urlencodedParser, index_c.force_join)



module.exports = router;
