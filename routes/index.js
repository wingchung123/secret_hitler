var express = require('express');
var router = express.Router();

let index_c = require('../controllers/index_controller')
/* GET home page. */
router.get('/', index_c.index);

module.exports = router;
