const express = require('express');
const app = express();
const path = require('path');
const exphbs  = require('express-handlebars');
const bodyParser = require('body-parser');
const {HttpReq} = require('./scripts/api.js');
const formula = require('./routes/formula')(__dirname);
app.use(bodyParser.urlencoded({
    extended: true
  }));

 const hbs = app.engine('.hbs', exphbs({
    extname: '.hbs',
    layoutsDir: path.join(__dirname, 'views', 'layouts'),
    partialsDir: path.join(__dirname, 'views', 'partials'),
    defaultLayout: 'main',
    helpers: {
        foo: function () {
            return "foo";
        }
    }
}));

app.engine('handlebars', hbs.engine);
app.set('view engine', 'hbs');
app.set('views', 'views');
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'public')));
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


app.listen(process.env.PORT ? process.env.PORT : 3000, () => console.log('Example app listening on port 3000!'));