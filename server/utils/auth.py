"""
This will do the main job of authenticating for logging in and
locks, locking and unlocking
"""

import time
import query

CONN = query.Query("pi", "329db", "localhost", "smart_lock")

def login(email, passwd):
    """
    selects a row that matches the given email and password,
    then returns the id if successfully authenticated. otherwise
    returns False
    """
    curs = CONN.select("id", "Users",
                       "email = '{}' and password = '{}'".format(email, passwd))
    if curs.rowcount == 0:
        return False
    return curs.fetchone()["id"]

def use_lock(user_id, lock_id, oper):
    """
    checks whether the given ID can activate
    the given lock
    user_id - id to check
    lock_id - lock to check
    oper - U or L for unlock or lock
    """
    curs = CONN.select("lock_id", "Perms",
                       "user_id = '{}' AND lock_id = '{}'".format(user_id, lock_id))

    if curs.rowcount == 0:
        # the given user doesn't have permission for this lock
        return False

    # we got this far, user has permission so log
    # the action in the db
    CONN.insert("Ops", "user_id, lock_id, time, op",
                "{}, {}, {}, {}".format(
                    user_id, lock_id, time.time(), oper))

    # now insert the new state of the lock
    CONN.gen_query("""insert into Locks columns (state)
                    values ({}) where id = '{}'""".format(
                        oper, lock_id))
    return True

def add_user_to_lock(owner_id, user_id, lock_id):
    """
    adds a user to the specified lock
    owner_id - owner of the lock
    user_id - user to be added
    lock_id - lock that the user is to be added to
    """
    curs = CONN.select("*", "Locks",
                       "id = '{}' AND owner_id = '{}'".format(lock_id, owner_id))
    if curs.rowcount == 0:
        # we don't have the correct owner
        return False
    # we have the correct owner, check if the user
    # already has permission
    curs = CONN.select("*", "Perms",
                       "lock_id = '{}' AND user_id = '{}'".format(lock_id, user_id))
    if curs.rowcount > 0:
        # they do, just return a success
        return True
    # they don't, so insert the permission into the db
    CONN.gen_query("""insert into Perms columns (lock_id, user_id)
                   values ({}, {})""".format(lock_id, user_id))
    return True

def create_account(email, passwd):
    """
    creates a new user in the database
    """
    curs = CONN.select("*", "Users",
                       "email = '{}'".format(email))
    if curs.rowcount > 0:
        # this email address is already registered
        return False
    CONN.insert("Users", "email, password",
                "{}, {}".format(email, passwd))
    # account was created, return the new user_id
    return login(email, passwd)
