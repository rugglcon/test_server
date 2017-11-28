var express = require('express'),
  request = require('request'),
  query = require('./utils/query.js'),
  auth = require('./utils/auth.js');
var app = express();

function handle_res(res, err, data) {
  if(!err) {
    res.send(JSON.stringify({error: 0, data: data}));
  } else {
    res.send(JSON.stringify({error: err, data: data}));
  }
}

app.get('/open_lock', function(req, res) {
  auth.use_lock(req.query.user_id, req.query.lock_id, 'U',
  function(err, data) {
    if(err) {
      return res.send(JSON.stringify({error: err, data: data}));
    } else {
      query.query("select * from Locks where id = " + req.query.lock_id,
        function(err, data) {
          if(err) {
            return res.send(JSON.stringify({error: err, data: data}));
          } else {
            var lock_ip = data[0].IP;
            request.get('http://0.0.0.0:8000' + '/open_lock',
              function(error, resp, body) {
                if(error) {
                  return res.send(JSON.stringify({error: error, data: body}));
                } else {
                  console.log(body);
                  res.send(JSON.stringify({error: 0, data: body}));
                }
            });
          }
      });
    }
  });
});

app.get('/close_lock', function(req, res) {
  auth.use_lock(req.query.user_id, req.query.lock_id, 'L',
    function(err, data) {
      if(err) {
        return res.send(JSON.stringify({error: err, data: data}));
      } else {
        query.query("select * from Locks where id = " + req.query.lock_id,
          function(err, data) {
            if(err) {
              return res.send(JSON.stringify({error: err, data: data}));
            } else {
              var lock_ip = data[0].IP;
              request.get('http://0.0.0.0:8000' + '/close_lock',
                function(error, resp, body) {
                  if(error) {
                    return res.send(JSON.stringify({error: error, data: body}));
                  } else {
                    console.log(body);
                    res.send(JSON.stringify({error: 0, data: body}));
                  }
              });
            }
        });
      }
  });
});

app.get('/login', function(req, res) {
  auth.login(req.query.email, req.query.password,
    function(err, data) {
      handle_res(res, err, data);
  });
});

app.get('/signup', function(req, res) {
  auth.create_account(req.query.email, req.query.password,
    function(err, data) {
      handle_res(res, err, data);
  });
});

app.get('/add_user_to_lock', function(req, res) {
  auth.add_user_to_lock(req.query.owner_id, req.query.user_id, req.query.lock_id,
    function(err, data) {
      handle_res(res, err, data);
  });
});

app.listen(8080, '0.0.0.0', function() {
  console.log('listening on port 8080');
});