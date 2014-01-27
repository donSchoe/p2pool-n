
// if you know of a better way or a public geolocation API, please modify this!

var http = require('http')

function Geo(options) {
    var self = this;
        
    function request(options, callback)
    {    
        http_handler = http;
        var req = http_handler.request(options, function(res) {
            res.setEncoding('utf8');
            var result = '';
            res.on('data', function (data) {
                result += data;
            });

            res.on('end', function () {
                callback(null, result);
            });
        });

        req.on('socket', function (socket) {
            socket.setTimeout(options.timeout);  
            socket.on('timeout', function() {
                req.abort();
            });
        });

        req.on('error', function(e) {
            callback(e);
        });

        req.end();
    }

    function extract_geo(html) {
       
        // if you have a better way of doing this
        // or know of a free geoip locator, then
        // please change this!

        html = html.replace(/[\r\n]/g, "");
        var b = html.match(/Country:.*absmiddle/gm);
        var c = b[0].match(/_blank.*\<\/a\>/g);
        var d = c[0]
        var country = d.substring(8,d.length-4);
        var e = b[0].match(/src=\'.*alt/g);
        var f = e[0];
        var img = "http://www.geoiptool.com/"+f.substring(6, f.length-5);
        
        var o = {
            country : country,
            img : img
        }

        return o;
    }

    self.get = function(ip, callback) {

        // console.log("QUERYING IP:",ip);
        var options = {
            host : 'www.geoiptool.com',
            port : 80,
            path: '/en/?IP='+ip,
            method: 'GET'
        }

        request(options, function(err, response) {
            if(err)
                return callback(err);
            var geo = null;
            try {
                var geo = extract_geo(response);
                // console.log(geo.country," ",geo.img);
            } catch(ex) {
                console.error(ex);
            }

            return callback(null, geo);

        }, true);
    }

}

module.exports = Geo;