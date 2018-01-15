const express = require('express');
const app = express();
const path = require('path');
const bodyParser = require('body-parser');
const {HttpReq} = require('./scripts/api.js');
const formula = require('./routes/formula')(__dirname);
app.use(bodyParser.urlencoded({
    extended: true
  }));
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'public')));
app.use('/formula',formula);

app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname + '/index.html'));
});

app.post('/compute', function(req, res) {
    HttpReq(req.body).then(data => res.send(data));
});

app.listen(process.env.PORT ? process.env.PORT : 3000, () => console.log('Example app listening on port 3000!'));