var mysql = require('mysql');

/**
 * @class Query
 */
function Query() {
  this.connection = mysql.createConnection({
    host     : 'localhost',
    user     : 'pi',
    password : '329db',
    database : 'smart_lock'
  });
  this.connection.connect();

  this.query = function(qs, callback) {
    this.connection.query(qs, function(err, rows, fields, dbq) {
      if(!err) {
        callback(0, rows);
      } else {
        callback(1, "Error: " + err);
      }
    });
  };
}

module.exports = new Query();
