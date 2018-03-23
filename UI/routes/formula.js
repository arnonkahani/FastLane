var express = require('express');
var router = express.Router();
const path = require('path');
// middleware that is specific to this router
const create_route = function(dirname){
    router.use(express.static(path.join(dirname, 'public')));
    router.get('/select', function(req, res) {
        res.render('select_formula');
    });

    router.get('/create', function(req, res) {
        res.render('create_formula');
    });



return router;
}

module.exports = dirname => create_route(dirname);