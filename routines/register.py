import requests
import rsa
import json


def routine(baseUrl):

    # User Data input
    print('Entre com os dados para efetuar um novo registro:')
    inputUsername = input("Usuário: ")
    inputPassword = input("Senha: ")

    # Serialize the data so it can be sent over the network
    usernameData = json.dumps({'username': inputUsername})

    # Make the request to generate user keys to this username
    result = requests.post(baseUrl + '/api/v1/user/generate',
                           data=usernameData)

    # Get back the result from the request to generate keys
    generateKeys = result.json()

    # Verify if keygen was successful.
    if generateKeys['success']:
        string_public_key = generateKeys['public_key']
        pkcs = string_public_key.encode('utf-8')
        public_key = rsa.PublicKey.load_pkcs1(pkcs, format='PEM')

        bytesUsername = inputUsername.encode('utf-8')
        bytesPassword = inputPassword.encode('utf-8')

        encryptedUsername = rsa.encrypt(bytesUsername, public_key)
        encryptedPassword = rsa.encrypt(bytesPassword, public_key)

        credentials = {
            'username': encryptedUsername.decode('latin1'),
            'password': encryptedPassword.decode('latin1')
        }

        credentialsJSON = json.dumps(credentials)

        requestData = json.dumps({
            'public_key': string_public_key,
            'credentials': credentialsJSON
        })

        result = requests.post(baseUrl + '/api/v1/user/register',
                               data=requestData)

    return result.json()