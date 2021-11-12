from rsa.pkcs1 import decrypt
from routines.login import routine as LOGIN_ROUTINE
from routines.register import routine as REGISTER_ROUTINE

# Base URL for API calls
baseUrl = 'http://localhost:5000'

# Test

# import rsa
# (pubKey, privKey) = rsa.newkeys(512)

# message = 'Some message.'.encode('utf-8')

# encryptedMessage = rsa.encrypt(message, pubKey)
# print(encryptedMessage)
# print('')

# stringfiedMessage = encryptedMessage.decode('latin1')
# print(stringfiedMessage)
# print("")

# encodedMessage = stringfiedMessage.encode('latin1')
# print(encodedMessage)
# print('')

# quit()


def procedureSelection():
    print(
        '[1] Logar com um usuário existente\n[2] Registrar um novo usuário.\n[3] Sair da aplicação.'
    )

    procedure = input('> ')

    if procedure == '1':
        result = LOGIN_ROUTINE(baseUrl)

        if result['success']:
            print('Usuário logado com sucesso.')
            quit()
        else:
            print(result['message'])
            procedureSelection()
    elif procedure == '2':
        result = REGISTER_ROUTINE(baseUrl)
        if result['success']:
            print('Usuário registrado com sucesso. Você pode logar agora.')
            procedureSelection()
        else:
            print(result['message'])
            procedureSelection()
    elif procedure == '3':
        print('A aplicação terminará agora.')
        quit()
    else:
        print('Você precisa selecionar uma das opções abaixo:')
        procedureSelection()


# User Procedure Selection
print('Selecione a rotina desejada entrando com o valor numérico da operação:')
procedureSelection()
