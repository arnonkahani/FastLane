const express = require('express');
const app = express();
const path = require('path');
var cookieParser = require('cookie-parser')
const exphbs  = require('express-handlebars');
const bodyParser = require('body-parser');
const uuidv1 = require('uuid/v1');
const {HttpReq} = require('./scripts/api.js');
const formula = require('./routes/formula')(__dirname);
const axios = require('axios')
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

      axios.defaults.headers.common['Access-Control-Allow-Origin'] = "*"
      axios({
          method: 'get',
          url: 'http://132.73.214.26:3000/compute',
          data: [[31.793292315858235,35.22995926314252],[31.791536887611592,35.23259812066226]]
        })
        .then(function (response) {
            console.log(response.data.data.stops)
          res.render('updatedVis3',{data_viz:response.data});
        })
        .catch(function (error) {
            res.send(error)
        });
    
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

     axios.defaults.headers.common['Access-Control-Allow-Origin'] = "*"
      axios({
          method: 'get',
          url: 'http://132.73.214.26:3000/compute',
          data: [[31.793292315858235,35.22995926314252],[31.791536887611592,35.23259812066226]]
        })
        .then(function (response) {
            stations_view = response.data.data.stops.map(x => x.stop_name)
          res.render('updatedVis1',{data_viz:response.data, stations:stations_view});
        })
        .catch(function (error) {
            res.send(error)
        });
});

app.get("/updatedVis2", function (req, res, next) {

      axios.defaults.headers.common['Access-Control-Allow-Origin'] = "*"
      axios({
          method: 'get',
          url: 'http://132.73.214.26:3000/compute',
          data: [[31.793292315858235,35.22995926314252],[31.791536887611592,35.23259812066226]]
        })
        .then(function (response) {
            stations_view = response.data.data.stops.map(x => x.stop_name)
          res.render('updatedVis2',{data_viz:response.data, stations:stations_view});
        })
        .catch(function (error) {
            res.send(error)
        });

    });

app.listen(process.env.PORT ? process.env.PORT : 3000, () => console.log('Example app listening on port 3000!'));