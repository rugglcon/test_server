"""
query module so the main file doesn't
need to worry about the database except
for the data that goes in and out.
"""

import mysql.connector

class Query:
    """query class for portability"""

    def __init__(self, user, password, host, db):
        self.conn = mysql.connector.connect(user=user, password=password,
                    host=host, database=db)

    def __del__(self):
        self.conn.close()

    def select(self, selector, table, where=""):
        """
        function to retrieve data from tables
        returns all the rows from the select

        selector - comma separated list of columns to select,
            or '*' for all
        table - table or comma separated list of tables to
            select from
        where - defaults to empty string to select all rows,
            otherwise takes 'where' condition for query
        """
        cursor = self.conn.cursor(buffered=True, dictionary=True)
        selection = "SELECT {} FROM {}".format(selector, table)
        if where != "":
            selection += " WHERE {}".format(where)
        cursor.execute(selection)
        return cursor

    def insert(self, table, columns, values, where=""):
        """
        inserts data into a given table
        returns True for success, False on Error

        table - string of the table to insert to
        columns - comma separated list of column names
        values - comma separated list of values
        """
        cursor = self.conn.cursor(buffered=True, dictionary=True)
        query = "INSERT INTO {} ({}) VALUES ({})".format(
            table, columns, values)

        if where != "":
            query += " WHERE {}".format(where)
        try:
            cursor.execute(query)
        except mysql.connector.Error:
            return False
        return True


    def gen_query(self, query_string):
        """
        general query function for unique queries
        returns False on Error, otherwise returns
            the cursor object
        """
        cursor = self.conn.cursor(buffered=True, dictionary=True)
        try:
            cursor.execute(query_string)
        except mysql.connector.Error:
            return False
        return cursor
