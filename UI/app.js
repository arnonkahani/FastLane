const express = require('express');
const app = express();
const path = require('path');
var cookieParser = require('cookie-parser')
const exphbs  = require('express-handlebars');
const bodyParser = require('body-parser');
const uuidv1 = require('uuid/v1');
const {HttpReq} = require('./scripts/api.js');
const formula = require('./routes/formula')(__dirname);

analytics_data = {}
analytics_data_movment = {}

app.use(bodyParser.urlencoded({
    extended: true
  }));

app.use(cookieParser())

 const hbs = app.engine('.hbs', exphbs({
    extname: '.hbs',
    layoutsDir: path.join(__dirname, 'views', 'layouts'),
    partialsDir: path.join(__dirname, 'views', 'partials'),
    defaultLayout: 'main',
    helpers: {
        foo: function () {
            return "foo";
        },
        json: function (content) {
    return JSON.stringify(content)
    }
    }
}));

app.engine('handlebars', hbs.engine);
app.set('view engine', 'hbs');
app.set('views', 'views');
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'public')));

app.use(function (req, res, next) {
    var cookie = req.cookies.cookieName;
    if (cookie === undefined)
    {
      res.cookie('cookieName',uuidv1(), { maxAge: 900000, httpOnly: true });
      console.log('cookie created successfully');
    } 
    else
    {
      console.log('cookie exists', cookie);
    } 
    next();
  });


app.use('/formula',formula);

app.get("/", function (req, res, next) {
    res.render('home');
});

app.get("/vis1", function (req, res, next) {
    res.render('vis1');
});

app.get("/vis2", function (req, res, next) {
    res.render('vis2');
});

app.get("/vis3", function (req, res, next) {
    res.render('vis3');
});

app.get("/updatedVis3", function (req, res, next) {
    res.render('updatedVis3');
});

app.post("/analytics", function(req, res, next){
    let analytics = req.body
    sessionId = req.cookies.cookieName
    analytics.time = new Date().getTime()
    if(analytics_data[sessionId]){
        analytics_data[sessionId].push(analytics)
    }else{
        analytics_data[sessionId] = [analytics]
    }


})


app.post("/analytics/movment", function(req, res, next){
    let analytics = req.body
    sessionId = req.cookies.cookieName
    analytics.time = new Date().getTime()
    if(analytics_data_movment[sessionId]){
        analytics_data_movment[sessionId] = analytics_data_movment[sessionId].concat(analytics.movment_data)
    }else{
        analytics_data_movment[sessionId] = [analytics.movment_data]
    }


})

app.get("/analytics", function (req, res, next) {
    analytics_view = []
    Object.entries(analytics_data).forEach(function(value, key, map){
    user = {sessionId: value[0],button_clicks: value[1].length}
    analytics_view.push(user)
    })

    movment_view = {}
    Object.entries(analytics_data_movment).forEach(function(value, key, map){
    movment_view[value[0]] = value[1]
    })

    console.log(analytics_data_movment)
    res.render('analytics',{data:analytics_view,movment_data:movment_view});
});


app.get("/updatedVis1", function (req, res, next) {

    res.render('updatedVis1',{stations:["\u05d3\u05d9\u05d6\u05e0\u05d2\u05d5\u05e3/\u05d2\u05d5\u05e8\u05d3\u05d5\u05df","\u05d3\u05d9\u05d6\u05e0\u05d2\u05d5\u05e3/\u05e9\u05d3' \u05d1\u05df \u05d2\u05d5\u05e8\u05d9\u05d5\u05df","\u05e9\u05d3' \u05d1\u05df \u05d2\u05d5\u05e8\u05d9\u05d5\u05df/\u05d3\u05d9\u05d6\u05e0\u05d2\u05d5\u05e3",
    "\u05e8\u05d9\u05d9\u05e0\u05e1/\u05d2\u05d5\u05e8\u05d3\u05d5\u05df"]});
});

app.get("/updatedVis2", function (req, res, next) {
    
        res.render('updatedVis2',{stations:["\u05ea\u05d7\u05e0\u05d4 \u05de\u05e8\u05db\u05d6\u05d9\u05ea \u05ea\u05dc \u05d0\u05d1\u05d9\u05d1 \u05e7\u05d5\u05de\u05d4 6/\u05e8\u05e6\u05d9\u05e4\u05d9\u05dd",
       "\u05e9\u05d3' \u05d4\u05e8 \u05e6\u05d9\u05d5\u05df/\u05d3\u05e8\u05da \u05e9\u05dc\u05de\u05d4",
       "\u05e9\u05d5\u05e7\u05df/\u05d1\u05e8 \u05d9\u05d5\u05d7\u05d0\u05d9",
       "\u05e9\u05d3' \u05e8\u05d5\u05d8\u05e9\u05d9\u05dc\u05d3/\u05e9\u05d9\u05d9\u05e0\u05e7\u05d9\u05df",
       "\u05d4\u05d7\u05e9\u05de\u05d5\u05e0\u05d0\u05d9\u05dd/\u05d9\u05d4\u05d5\u05d3\u05d4 \u05d4\u05dc\u05d5\u05d9",
       "\u05d4\u05e1\u05d9\u05e0\u05de\u05d8\u05e7/\u05e7\u05e8\u05dc\u05d9\u05d1\u05da",
       "\u05d0\u05d1\u05df \u05d2\u05d1\u05d9\u05e8\u05d5\u05dc/\u05e7\u05e8\u05dc\u05d9\u05d1\u05da",
       "\u05d0\u05d1\u05df \u05d2\u05d1\u05d9\u05e8\u05d5\u05dc/\u05e9\u05d3' \u05e9\u05d0\u05d5\u05dc \u05d4\u05de\u05dc\u05da",
       "\u05d4\u05e9\u05d5\u05de\u05e8\u05d5\u05df/\u05e9\u05d3' \u05d4\u05e8 \u05e6\u05d9\u05d5\u05df",
       "\u05ea\u05d7\u05e0\u05d4 \u05de\u05e8\u05db\u05d6\u05d9\u05ea \u05ea''\u05d0/\u05dc\u05d5\u05d9\u05e0\u05e1\u05e7\u05d9",
       "\u05ea\u05d7\u05e0\u05d4 \u05de\u05e8\u05db\u05d6\u05d9\u05ea \u05ea\u05dc \u05d0\u05d1\u05d9\u05d1 \u05e7\u05d5\u05de\u05d4 4/\u05d4\u05d5\u05e8\u05d3\u05d4",
       "\u05d0\u05dc\u05e0\u05d1\u05d9/\u05dc\u05d9\u05dc\u05d9\u05e0\u05d1\u05dc\u05d5\u05dd",
       "\u05d3\u05e8\u05da \u05e9\u05dc\u05de\u05d4/\u05e9\u05d3' \u05d4\u05e8 \u05e6\u05d9\u05d5\u05df",
       "\u05d1\u05d9''\u05e1 \u05e9\u05d1\u05d7 \u05de\u05d5\u05e4\u05ea/\u05d4\u05de\u05e1\u05d2\u05e8",
       "\u05d4\u05e9\u05dc\u05d5\u05dd",
       "\u05ea\u05dc \u05d0\u05d1\u05d9\u05d1 \u05d4\u05d4\u05d2\u05e0\u05d4",
       "\u05de\u05e1\u05d5\u05e3 2000/\u05e2\u05dc\u05d9\u05d4",
       "\u05ea\u05d7\u05e0\u05d4 \u05de\u05e8\u05db\u05d6\u05d9\u05ea \u05ea\u05dc \u05d0\u05d1\u05d9\u05d1 \u05e7\u05d5\u05de\u05d4 6/\u05e8\u05e6\u05d9\u05e4\u05d9\u05dd",
       "\u05ea\u05d7\u05e0\u05d4 \u05de\u05e8\u05db\u05d6\u05d9\u05ea \u05ea\u05dc \u05d0\u05d1\u05d9\u05d1 \u05e7\u05d5\u05de\u05d4 7/\u05e8\u05e6\u05d9\u05e4\u05d9\u05dd",
       "\u05d0\u05d1\u05df \u05d2\u05d1\u05d9\u05e8\u05d5\u05dc/\u05de\u05d0\u05e0\u05d4",
       "\u05db\u05d9\u05db\u05e8 \u05d4\u05e9\u05e2\u05d5\u05df/\u05de\u05e8\u05d6\u05d5\u05e7 \u05d5\u05e2\u05d6\u05e8"]});
    });

app.listen(process.env.PORT ? process.env.PORT : 3000, () => console.log('Example app listening on port 3000!'));