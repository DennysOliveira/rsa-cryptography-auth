import sqlite3
from sqlite3.dbapi2 import Cursor
import requests
import json


class Database:
    __instance = None
    conn = None
    cursor = None

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            cls.__instance = cls
        return cls.__instance

    @classmethod
    def connect(cls, file):
        if not cls.conn:
            print('Creating db connection...')
            cls.conn = sqlite3.connect(file, check_same_thread=False)
        if not cls.cursor:
            cls.cursor = cls.conn.cursor()
        return cls.conn

    @classmethod
    def disconnect(cls):
        return cls.conn.close()

    @classmethod
    def validateUser(cls, username):
        sql = "SELECT * FROM users WHERE username = '{}'".format(username)
        result = cls.cursor.execute(sql).fetchone()

        if result:
            return True
        else:
            return False

    @classmethod
    def registerKeys(cls, username, keys):
        # Check if we received a username
        if username:
            # Check if the user already exists before trying to create it.
            registered = cls.validateUser(username)
            print('Is user registered? ' + str(registered))

            # If not registered:
            if (not registered):

                sql = "INSERT INTO users VALUES('{}','null','{}', '{}')".format(
                    username, keys['public_key'], keys['private_key'])

                cls.cursor.execute(sql)

                result = cls.cursor.execute(
                    "SELECT * FROM users WHERE username ='{}'".format(
                        username)).fetchone()

                print('Database registerKeys public_key recvd:')
                print(keys['public_key'].encode('utf-8'))

                if result:
                    cls.conn.commit()
                    return json.dumps({
                        'success': True,
                        'registered': True,
                        'message': 'Succeeded on creating this user.',
                        'public_key': keys['public_key']
                    })
                else:
                    return json.dumps({
                        'success': False,
                        'registered': False,
                        'message': 'Could not create user.'
                    })
            else:
                return json.dumps({
                    'success': False,
                    'registered': True,
                    'message': 'User already exists.'
                })
        else:
            return json.dumps({
                'success': False,
                'registered': False,
                'message': 'Not enough parameters received.'
            })

    @classmethod
    def registerPassword(cls, credentials):
        sql = "UPDATE users SET password='{}' WHERE username='{}'".format(
            credentials['password'], credentials['username'])

        print('Credentials in registerPassword')
        print(credentials)

        result = cls.cursor.execute(sql)

        validationSQL = 'SELECT * FROM users WHERE username="{}"'.format(
            credentials['username'])

        validation = cls.cursor.execute(validationSQL).fetchone()

        print('validation')
        print(validation)
        if validation[1]:
            cls.conn.commit()
            return True
        else:
            return False

    @classmethod
    def loadPrivateKey(cls, public_key):
        sql = "SELECT * FROM users WHERE public_key = '{}'".format(public_key)
        result = cls.cursor.execute(sql)

        if result:
            return (result.fetchone()[3])
        else:
            return False