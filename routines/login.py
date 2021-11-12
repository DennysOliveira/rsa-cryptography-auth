import requests
from requests.api import get
import rsa
import json
from getpass import getpass


def routine(baseUrl):
    # User Data Input as string
    print('Entre com as suas credenciais:')
    inputUsername = input("Usuário: ")
    inputPassword = getpass("Senha: ")

    # If one of those are not provided, return the error to the user
    # Se uma das opções não forem fornecidas, retorna o erro para o usuário
    if ((not inputUsername) or (not inputPassword)):
        return {
            'success': False,
            'message': 'Erro: Você precisa entrar com um usuário e senha.'
        }

    # Stringify username data for it to be able to be sent over the network
    validationData = json.dumps({'username': inputUsername})

    # Make the request to the validation endpoint
    # This endpoint returns if the user exists.
    # If it does, it also returns user 'public_key' as a pkcs PEM string
    print('Carregando...')
    result = requests.get(baseUrl + '/api/v1/user/validate',
                          headers={'content-type': 'application/json'},
                          data=validationData)

    # Parse the request result data into an dictionary
    validation = result.json()

    # If the user exists::
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

        # Create the user object to be sent over the network
        # Cria o objeto do usuário para ser enviado para a validação de credenciais
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