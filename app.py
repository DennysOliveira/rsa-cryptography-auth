from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import requests
import rsa
from rsa.key import PrivateKey
from database import Database
import json
from types import SimpleNamespace

app = Flask("api")
api = Api(app)

try:
    database = Database().get_instance()
    conn = database.connect(r'./database/users.db')
except Exception as exception:
    print("Exception found. Quitting.")
    print("Exception: {}".format(exception))
    quit()


@app.route('/api/v1/user/authenticate', methods=['POST'])
def authenticate():
    if not (request.data):
        return json.dumps({
            'success': False,
            'message': 'Invalid credentials received.'
        })

    # Loads request data into a dictionary from JSON received.
    data = json.loads(request.data)

    # Unpack data received
    string_public_pkcs = data[
        'public_key']  # Public key pkcs decoded in 'utf-8'
    string_credentials = data['credentials']  # Credentials decoded in 'latin1'

    # Load the loadable string from the database for the current user
    string_private_pkcs = database.loadPrivateKey(string_public_pkcs)

    if not (string_private_pkcs):
        return json.dumps({
            'success': False,
            'message': 'Could not find private key.'
        })

    bytes_private_pkcs = string_private_pkcs.encode('utf-8')

    userPrivateKey = rsa.PrivateKey.load_pkcs1(bytes_private_pkcs,
                                               format='PEM')

    bytes_encrypted_credentials = string_credentials.encode('latin1')

    bytes_decrypted_credentials = rsa.decrypt(bytes_encrypted_credentials,
                                              userPrivateKey)

    clear_credentials = json.loads(
        bytes_decrypted_credentials.decode('latin1'))

    authentication = database.validatePassword(clear_credentials)

    print('User authenticated. Valid credentials received.')
    print(authentication)

    return json.dumps(authentication)


@app.route('/api/v1/user/validate', methods=['GET'])
def verifyUser():
    if (not request.data):
        return json.dumps({
            "status": False,
            'message': 'No data was provided.'
        })

    user = json.loads(request.data)

    print('Verifying if the user exists -> ' + user['username'])
    result = database.validateUser(user['username'])

    print('Database validation result = ' + str(result['status']))

    return json.dumps(result)

    # if (result):
    #     return json.dumps({"status": result, "public_key": result[2]})
    # else:
    #     return json.dumps({"status": False})


@app.route('/api/v1/user/generate', methods=['POST'])
def generateKeypair():
    if not request.data:
        return json.dumps({
            'success': False,
            'message': 'Blank data was given.'
        })

    # Loads the received parameters into a Dictionary
    data = json.loads(request.data)

    # Verify if username was provided.
    try:
        username = data['username']

        if not username:
            return json.dumps({
                'success': False,
                'message': 'No username was provided.'
            })
    except:
        return json.dumps({
            'success': False,
            'message': 'No username was provided.'
        })

    # userExists = database.validateUser(username)

    print('Data received: ')
    (newPublicKey, newPrivateKey) = rsa.newkeys(512)
    public_pkcs = newPublicKey.save_pkcs1(format='PEM')
    private_pkcs = newPrivateKey.save_pkcs1(format='PEM')

    string_public_pkcs = public_pkcs.decode('utf-8')
    string_private_pkcs = private_pkcs.decode('utf-8')

    keys = {
        'public_key': string_public_pkcs,
        'private_key': string_private_pkcs
    }

    print('Making the request to the database.')
    databaseRequest = database.registerKeys(username, keys)

    result = json.loads(databaseRequest)

    if (result['success']):
        print('Database successfully registered username and keypair.')
        return json.dumps(result)
    else:
        print('Could not generate keypair.')
        return json.dumps(result)


# [POST] /api/v1/user/register
# Endpoint responsável por finalizar o registro do usuário que já tem o par de chaves gerado.
@app.route('/api/v1/user/register', methods=['POST'])
def registerUser():
    if (not request.data):
        return json.dumps({
            'success': False,
            'message': 'You need to provide data.'
        })

    # Loads the received parameters into a Dictionary
    data = json.loads(request.data)

    print('Data received from client request /register')
    print(data)

    # Unpack data received from client request
    string_public_pkcs = data['public_key']
    userCredentials = json.loads(data['credentials'])

    print('userCredentials, encrypted:')
    print(userCredentials)

    # Grab user private key string from database
    string_private_pkcs = database.loadPrivateKey(string_public_pkcs)
    print("Loading private key from database...")

    # Load the private key
    if (string_private_pkcs):
        # Encode it to bytes before loading pkcs
        bytes_private_pkcs = string_private_pkcs.encode('utf-8')
        # Load it as a AbstractKey
        userPrivateKey = rsa.PrivateKey.load_pkcs1(bytes_private_pkcs,
                                                   format='PEM')
    else:
        # Se as chaves não foram carregadas corretamente
        # If keys couldn't be loaded for some reason
        return json.dumps({
            'success': False,
            'message': 'Invalid or missing public key.'
        })

    # Encode credentials using the same method as client so they can be decrypted
    # RSA Encryption accepts only bytes, so it is needed to encode the 'message'
    bytesCredentials = {
        'username': userCredentials['username'].encode('latin1'),
        'password': userCredentials['password'].encode('latin1')
    }

    # Decrypt Credentials received from client
    decryptedCredentials = {
        'username': rsa.decrypt(bytesCredentials['username'], userPrivateKey),
        'password': rsa.decrypt(bytesCredentials['password'], userPrivateKey)
    }

    print(decryptedCredentials)

    # Validate unpacked data
    try:
        clearCredentials = {
            "username": decryptedCredentials['username'].decode('utf-8'),
            "password": decryptedCredentials['password'].decode('utf-8')
        }

        if not (clearCredentials['username'] and clearCredentials['password']):
            return json.dumps({
                'success': False,
                'message': 'Missing username or password.'
            })
    except:
        return json.dumps({
            'success': False,
            'message': 'Not enough parameters received.'
        })

    result = database.registerPassword(clearCredentials)

    if result:
        return json.dumps({
            'success': True,
            'message': 'User registered successfully.'
        })
    else:
        return json.dumps({
            'success':
            False,
            'message':
            'Something happened when contacting the database.'
        })


@app.route('/api/v1/database/sql/execute', methods=['POST'])
def executeSQL():
    data = json.loads(request.data.decode(),
                      object_hook=lambda d: SimpleNamespace(**d))
    sql = data.sql
    # sql = 'CREATE TABLE users (username VARCHAR(255), password VARCHAR(MAX), publickey VARCHAR(MAX), privatekey VARCHAR(MAX))'
    try:
        result = database.cursor.execute(sql)
        for x in result:
            print(x)

        database.conn.commit()
        return json.dumps("SQL Executed Successfully.")
    except Exception as exception:
        print(exception)
        return json.dumps(str(exception))


@app.route('/api/v1/rsa/newkeys', methods=['GET'])
def newKeys():
    (newPublic, newPrivate) = rsa.newkeys(512)
    return json.dumps({
        "public_key": str(newPublic),
        "private_key": str(newPrivate)
    })


if (__name__ == "__main__"):
    app.run()