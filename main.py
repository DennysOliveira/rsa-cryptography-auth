# Desacoplamento de funções
from routines.login import routine as LOGIN_ROUTINE
from routines.register import routine as REGISTER_ROUTINE

# URL base da API que está rodando no Flask.
# Base URL for API Endpoints that are running on Flask.
baseUrl = 'http://localhost:5000'


# Recursive function that manages User input on routine selection.
# Função recursiva que administra a entrada do usuário na seleção das rotinas.
def procedureSelection():
    print(
        '[1] Logar com um usuário existente\n[2] Registrar um novo usuário.\n[3] Sair da aplicação.'
    )

    # Receives user input and calls routines accordingly.
    # Recebe a entrada do usuário para chamar as rotinas de acordo com o solicitado.
    procedure = input('> ')

    if procedure == '1':
        # Login routine handles user authentication based on correct credentials given
        result = LOGIN_ROUTINE(baseUrl)

        if result['success']:
            print('Usuário autenticado com sucesso.')
            quit()
        else:
            print(result['message'])
            print('')
            procedureSelection()
    elif procedure == '2':
        # Login routine handles user register into the db
        result = REGISTER_ROUTINE(baseUrl)
        if result['success']:
            print('Usuário registrado com sucesso. Você pode logar agora.')
            procedureSelection()
        else:
            print(result['message'])
            print('')
            procedureSelection()
    elif procedure == '3':
        print('A aplicação terminará agora.')
        quit()
    else:
        print('')
        print('Você precisa selecionar uma das opções abaixo:')
        procedureSelection()


# First recursive function call
print('Selecione a rotina desejada entrando com o valor numérico da operação:')
procedureSelection()
