const rp = require('request-promise');

 const HttpReq = async (body) => {

    var options = {
        url: 'http://132.72.233.203:3000/compute',
        body,
        json: true
    };

    const res = await rp(options);
    return res;
};

module.exports = {HttpReq};


