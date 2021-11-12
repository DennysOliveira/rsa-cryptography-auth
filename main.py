from rsa.pkcs1 import decrypt
from routines.login import routine as LOGIN_ROUTINE
from routines.register import routine as REGISTER_ROUTINE

# Base URL for API calls
baseUrl = 'http://localhost:5000'


def procedureSelection():
    print('')
    print(
        '[1] Logar com um usuário existente\n[2] Registrar um novo usuário.\n[3] Sair da aplicação.'
    )

    procedure = input('> ')

    if procedure == '1':
        result = LOGIN_ROUTINE(baseUrl)

        if result['success']:
            print('Usuário autenticado com sucesso.')
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
