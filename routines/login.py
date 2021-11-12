import requests
from requests.api import get
import rsa
import json
from getpass import getpass


def routine(baseUrl):
    # User Data input
    print('Entre com as suas credenciais:')
    inputUsername = input("Usuário: ")
    inputPassword = getpass("Senha: ")

    if ((not inputUsername) or (not inputPassword)):
        return {
            'success': False,
            'message': 'Erro: Você precisa entrar com um usuário e senha.'
        }

    validationData = json.dumps({'username': inputUsername})

    # Make the request
    print('Carregando...')
    result = requests.get(baseUrl + '/api/v1/user/validate',
                          headers={'content-type': 'application/json'},
                          data=validationData)

    # Parse the result data into an dictionary
    validation = result.json()

    # quit()
    if (validation['status']):
        # Instantiate a RSA Public Key for the valid user
        public_key = rsa.PublicKey.load_pkcs1(validation['public_key'],
                                              format='PEM')

        # Create User Credentials as JSON and encode it to be able to be encrypted
        credentials = json.dumps({
            'username': inputUsername,
            'password': inputPassword
        }).encode('latin1')

        # Encrypt user credentials with user Public Key
        encryptedCredentials = rsa.encrypt(credentials, public_key)

        # Serialize credentials so it can be sent safely over then network
        stringCredentials = encryptedCredentials.decode('latin1')

        # Create the user object
        user_object = {
            'public_key': validation['public_key'],
            'credentials': stringCredentials
        }

        # Dumps user object into JSON data so we can make the request
        userData = json.dumps(user_object)

        # Send a request to the Authentication Endpoint with the encrypted user data
        authResult = requests.post(
            baseUrl + '/api/v1/user/authenticate',
            headers={'content-type': 'application/json'},
            data=userData)

        # Get back the request data and process it to a dict
        authData = authResult.json()

        if authData['success']:
            # Return the authentication status to the user
            return {
                'success': authData['success'],
                'message': 'Usuário autenticado com sucesso.'
            }
        else:
            return {
                'success': False,
                'message': 'Usuário ou senha incorretos.'
            }
    else:
        return {'success': False, 'message': 'Usuário ou senha incorretos.'}