from tabulate import tabulate

# MENU
menu = """
SISTEMA BANKSYSTEM

Selecione a opção desejada:

[1] Cadastrar cliente
[2] Cadastrar conta
[3] Consultar cadastro
[4] Ver clientes cadastrados
[5] Saque
[6] Depósito
[7] Extrato
[0] Sair

// """

# VARIÁVEIS
AGENCIA = '0001'
SALDO_INICIAL = 0
saldo = SALDO_INICIAL
numero_saques = 0
LIMITE_SAQUES = 3
historial_saques = []
historial_depositos = []
suma_saque = 0
suma_deposito = 0
saque = 0
deposito = 0
numero_conta = 0
cpf_consulta = 0
cpf_a_cadastrar = 0
extrato = 0
conta = 0

# FUNÇÕES

def cadastrar_clientes(clientes, cpf, nome, data_nascimento, endereco):
    if cpf not in clientes:
        clientes[cpf] = {
            "Nombre": nome,
            "Data de nascimento": data_nascimento,
            "Endereço": endereco
                }
        print('Cliente cadastrado com sucesso')
    else:
        print("Cliente já registrado")
cadastro_de_clientes = {}

def verificar_registro_cliente(cadastro_de_clientes, cpf):
    if cpf in cadastro_de_clientes:
        return True
    else:
        return False

def cadastrar_conta(lista_contas, cpf_a_cadastrar):
    print('CADASTRO DE CONTAS')
    cpf_a_cadastrar = input('Informe o CPF (somente números): ')
    cliente_registrado = verificar_registro_cliente(cadastro_de_clientes, cpf)
    if cliente_registrado:
        global AGENCIA
        numero_conta = len(lista_contas) + 1
        saldo = 0.0  # Agrega el saldo inicial aquí
        numero_saques = 0  # Agrega el número de saques inicial aquí
        lista_contas.append({"Agência": AGENCIA, "Número de conta": numero_conta, "Saldo": saldo, "Saques Realizados": numero_saques})
        print(f'Conta Ag: {AGENCIA} CC: {numero_conta} cadastrada com sucesso para o CPF {cpf} com limite de {LIMITE_SAQUES} saques diarios')
        if cpf in cadastro_de_clientes:
            if "Contas Bancárias" not in cadastro_de_clientes[cpf]:
                cadastro_de_clientes[cpf]["Contas Bancárias"] = []
            cadastro_de_clientes[cpf]["Contas Bancárias"].append({"Agência": AGENCIA, "Número de conta": numero_conta, "Saldo": saldo, "Saques Realizados": numero_saques})
    else:
        print('Cliente não cadastrado no sistema')
lista_contas = []

def consultar_cpf(cpf):
    print('CONSULTAR CADASTRO INDIVIDUAL')
    cpf = input('Informe o CPF a ser consultado (somente números): ')
    if cpf in cadastro_de_clientes:
        cliente = cadastro_de_clientes[cpf]
        tabela = tabulate([cliente.values()], headers=["Nome", "Data de Nascimento", "Endereço", "Contas Bancárias"], tablefmt="grid")
        print(tabela)

    else:
        print("Não existem registros em sistema")

def consultar_registros():
    print('CONSULTAR TODOS OS REGISTROS')
    tabela_clientes = []
    for cpf, cliente in cadastro_de_clientes.items():     
        tabela_clientes.append([cpf] + list(cliente.values()))
    if tabela_clientes:
        cabecalhos = ['CPF'] + list(cadastro_de_clientes[next(iter(cadastro_de_clientes))].keys())
        tabela = tabulate(tabela_clientes, headers=cabecalhos, tablefmt="grid")
        print(tabela)
    else:
        print("Não existem registros em sistema")

def sacar(cadastro_de_clientes, cpf, numero_conta, numero_saques, saque):
    print('SAQUE')
    cpf = input('Informe o CPF do titular (somente números): ')
    numero_conta = int(input('Informe o número da conta: '))
    if cpf in cadastro_de_clientes and "Contas Bancárias" in cadastro_de_clientes[cpf]:
        conta_encontrada = None
        for lista_contas in cadastro_de_clientes[cpf]["Contas Bancárias"]:
            if lista_contas["Número de conta"] == numero_conta:
                conta_encontrada = lista_contas
                break
        if conta_encontrada:
            if conta_encontrada["Saques Realizados"] >= LIMITE_SAQUES:
                print('O limite de saques foi atingido. Aguarde até amanhã para realizar novos saques')
            else:
                saque = float(input('Informe o valor para saque: R$'))
                if saque < 0:
                    print('Valor inválido para saque')
                else:
                    if conta_encontrada['Saldo'] >= saque:
                        conta_encontrada['Saldo'] -= saque
                        conta_encontrada['Saques Realizados'] += 1
                        print(f'Saque de número {conta_encontrada["Saques Realizados"]} por R${saque:.2f} realizado na conta {numero_conta}. Saldo atual: R${conta_encontrada["Saldo"]}')
                        if f'Historial de Saques {numero_conta}' not in conta_encontrada:
                            conta_encontrada[f'Historial de Saques {numero_conta}'] = []
                        if f"Historial de Depósitos {numero_conta}" not in conta_encontrada:
                            conta_encontrada[f"Historial de Depósitos {numero_conta}"] = []
                        conta_encontrada[f"Historial de Saques {numero_conta}"].append(saque)
                        conta_encontrada[f"Historial de Depósitos {numero_conta}"].append(0.0)
                        global suma_saque
                        suma_saque += saque
                    else:
                        print('Operação não realizada. Saldo insuficiente.')
        else:
            print('Número de conta não encontrado')
    else:
        print('Cliente não encontrado ou sem conta bancária')

def depositar(cadastro_de_clientes, cpf, numero_conta, deposito):
    print('DEPÓSITO')
    cpf = input('Informe o CPF do titular (somente números): ')
    numero_conta = int(input('Informe o número da conta: '))

    if cpf in cadastro_de_clientes and "Contas Bancárias" in cadastro_de_clientes[cpf]:
        conta_encontrada = None
        for lista_contas in cadastro_de_clientes[cpf]["Contas Bancárias"]:
            if lista_contas["Número de conta"] == numero_conta:
                conta_encontrada = lista_contas
                break
        if conta_encontrada:
            deposito = float(input('Informe o valor a depositar: R$'))
            if deposito < 0:
                print('Valor inválido para depósito')
            else:
                conta_encontrada['Saldo'] += deposito
                print(f"Depósito de R${deposito:.2f} realizado na conta {numero_conta}. Saldo atual: R${conta_encontrada['Saldo']}")
                if f"Historial de Depósitos {numero_conta}" not in conta_encontrada:
                    conta_encontrada[f"Historial de Depósitos {numero_conta}"] = []
                if f"Historial de Saques {numero_conta}" not in conta_encontrada:
                    conta_encontrada[f"Historial de Saques {numero_conta}"] = []
                conta_encontrada[f"Historial de Depósitos {numero_conta}"].append(deposito)
                conta_encontrada[f"Historial de Saques {numero_conta}"].append(0.0)
        else:
            print('Número de conta não encontrado)')
    else:
        print("Cliente não encontrado ou sem conta bancária") 

def exibir_extrato(cpf, numero_conta):
    print('EXTRATO BANCÁRIO')

    cpf = input('Informe o CPF (somente números): ')
    numero_conta = int(input('Informe o número da conta corrente: '))
    if cpf in cadastro_de_clientes and "Contas Bancárias" in cadastro_de_clientes[cpf]:
        conta_selecionada = None
        for conta in cadastro_de_clientes[cpf]["Contas Bancárias"]:
            if conta["Número de conta"] == numero_conta:
                conta_selecionada = conta
                break
        if conta_selecionada:
            saldo_inicial = SALDO_INICIAL
            historial_depositos = conta_selecionada.get(f'Historial de Depósitos {numero_conta}', [])
            historial_saques = conta_selecionada.get(f'Historial de Saques {numero_conta}', [])

            suma_deposito = sum(historial_depositos)
            suma_saque = sum(historial_saques)

            cabecalho = ["Depósitos", "Saques"]
            extrato = list(zip(historial_depositos, historial_saques))
            historico = tabulate(extrato, headers=cabecalho, tablefmt="grid")

            print()
            print(f'CPF {cpf} - AG {conta_selecionada["Agência"]} - CC {numero_conta}')
            print(f'Saldo inicial:     R${saldo_inicial:.2f}')
            print()
            if extrato:
                print(historico)
                print()
            print(f'Total de depósitos: R${suma_deposito:.2f}')
            print(f'Total de saques:   -R${suma_saque:.2f}')
            saldo_final = saldo_inicial + suma_deposito - suma_saque
            print(f'Saldo da conta:     R${saldo_final:.2f}')
        else:
            print("Conta não encontrada para o CPF e número de conta informados")
    else:
        print("Cliente não cadastrado no sistema ou não possui contas bancárias")



# PROGRAMA

while True:

    opcao = input(menu)

    if opcao == "1": # Cadastro de clientes 
        print('CADASTRO DE CLIENTES')
        cpf = input('Informe o CPF (somente números): ')
        cliente_registrado = verificar_registro_cliente(cadastro_de_clientes, cpf)
        if cliente_registrado:
            print('Cliente já cadastrado em sistema')
        else:
            nome = input('Informe o primeiro e último nome do cliente: ')
            data_nascimento = input('Informe a data de nascimento no formato DD/MM/AAAA: ')
            endereco = input('Informe o endereço no formato: Logradouro - Número - Bairro - Cidade/Estado: "\n"')
            cadastrar_clientes(cadastro_de_clientes, cpf, nome, data_nascimento, endereco)
    
    elif opcao == "2": # Cadastro de conta finalizada
        cadastrar_conta(lista_contas, cpf_a_cadastrar)

    elif opcao == "3": # Consultar CPF finalizada
        consultar_cpf(cpf)

    elif opcao == "4": #Consultar clientes cadastrados finalizada
        consultar_registros()

    elif opcao == "5": # Operação de saque finalizada
        sacar(cadastro_de_clientes, cpf, numero_conta, numero_saques, saque)

    elif opcao == "6": # Operação de depósito finlizada
        depositar(cadastro_de_clientes, cpf, numero_conta, deposito)

    elif opcao == "7": # Extrato finalizado
        exibir_extrato(cpf, numero_conta)

    elif opcao == "0": # Sair finalizado
        print('Muito obrigado pela preferência. Tenha um bom dia.')
        break
    
    else: # Erro finalizado
        print("Operação inválida, por favor selecione novamente a operação desejada")



            


           