import requests
import rsa
import json


def routine(baseUrl):

    # User Data input
    print('Entre com as suas credenciais:')
    inputUsername = input("Usuário: ")
    inputPassword = input("Senha: ")

    validationData = json.dumps({'username': inputUsername})

    # Make the request
    print('Making the request to User Validation Endpoint.')
    result = requests.get(baseUrl + '/api/v1/user/validate',
                          headers={'content-type': 'application/json'},
                          data=validationData)

    # Parse the result data into an dictionary
    print('Parsing the result data from the last request.')
    data = result.json()

    print('User exists: ' + str(data['status']))

    # quit()
    if (data['status']):
        # Instantiate a RSA Public Key for the valid user
        public_key = rsa.PublicKey().load_pkcs1(data['public_key'],
                                                format='DER')

        # Create User Credentials as JSON and encode it to be able to be encrypted
        credentials = json.dumps({
            'username': inputUsername,
            'password': inputPassword
        }).encode('utf-8')

        # Encrypt user credentials with user Public Key
        encryptedCredentials = rsa.encrypt(credentials, public_key)

        # Create the user object
        user_object = {
            'public_key': data['public_key'],
            'credentials': encryptedCredentials
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

        # Return the authentication status to the user
        print(authData['message'])
    else:
        print('Invalid username or password.')

    # (pubK, privK) = rsa.newkeys(512)
    # savedPubK = pubK.save_pkcs1(format='DER')
    # print('Saved Public Key:')
    # print(savedPubK)
    # print(type(savedPubK))

    # loadedPubK = rsa.PublicKey.load_pkcs1(savedPubK, format='DER')

    # print('Loaded Public Key:')
    # print(loadedPubK)
    # print(type(loadedPubK))