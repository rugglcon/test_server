var query = require('./query.js');

module.exports.login = function (email, passwd, callback) {
  query.query("select * from Users where email = '" + email + "' and password = '" + passwd + "'", function(err, data) {
      if(!err) {
        if(data.length == 0) {
          return callback(2, "No user with that email or password");
        }
        var usr_id = data[0].id;
        var usr_data = {};
        query.query("select lock_id from Perms where user_id = " + data[0].id,
          function(err, data) {
            var usr_locks = [];
            for(var i = 0; i < data.length; i++) {
              usr_locks[i] = {'lock_id': data[i].lock_id};
            }
            usr_data = {
              "user_id": usr_id,
              "locks": usr_locks
            };
            callback(0, usr_data);
          });
      } else {
        return callback(err, "Error: " + data);
      }
    });
};

module.exports.use_lock = function(user_id, lock_id, oper, callback) {
  query.query("select lock_id from Perms where user_id = " + user_id + " and lock_id = " + lock_id, function(err, data) {
    if(!err) {
      if(data.length == 0) {
        return callback(2, "User " + user_id + " doesn't have permissions for lock " + lock_id);
      }
      query.query("insert into Ops (user_id, lock_id, time, op) values ('" + user_id + "', '" + lock_id + "', NOW(), '" + oper + "')",
      function(err, data) {
        if(!err) {
          query.query("update Locks set state = '" + oper + "' where id = " + lock_id, function(err, data) {
            if(err) {
              return callback(err, "Error: " + data);
            } else {
              return callback(0, data);
            }
          });
        } else {
          return callback(err, "Error: " + data);
        }
      });
    } else {
      return callback(err, "Error: " + data);
    }
  });
};

module.exports.add_user_to_lock = function(owner_id, user_id, lock_id, callback) {
  query.query("select * from Locks where id = '" + lock_id + "' and owner_id = '" + owner_id + "'", function(err, data) {
    if(!err) {
      if(data.length == 0) {
        return callback(2, "Wrong owner for lock " + lock_id);
      }
      query.query("select * from Perms where lock_id = '" + lock_id + "' and user_id = '" + user_id + "'", function(err, data) {
        if(!err) {
          if(data.length == 0) {
            query.query("insert into Perms (lock_id, user_id) values ('" + lock_id + "', '" + user_id + "')", function(err, data) {
              if(err) {
                return callback(err, "Error: " + data);
              }
            });
          }
        }
      });
    } else {
      return callback(err, "Error: " + data);
    }
  });
};

module.exports.create_account = function(email, passwd, callback) {
  query.query("select * from Users where email = '" + email + "'",
  function(err, data) {
    if(!err) {
      if(data.length == 0) {
        query.query("insert into Users (email, password) values ('" + email + "', '" + passwd + "')", function(err, data) {
          if(err) {
            return callback(err, "Error: " + data);
          } else {
            module.exports.login(email, passwd, function(err, data) {
              if(err) {
                return callback(err, "Error: " + data);
              } else {
                return callback(0, data);
              }
            });
          }
        });
      } else {
        return callback(2, "User already exists with email " + email);
      }
    }
  });
};