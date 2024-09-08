"""
	Sistema Bancário Simples:
	- EXTRATO
	- DEPOSITO
	- SAQUE
	- CRIAR USUARIO
	- CRIAR CONTA
	- LISTAR CONTAS
"""

def verificar_usuario(lista_usuarios, *, cpf):
	lista_usuario_existente = [usuario for usuario in lista_usuarios if usuario['cpf'] == cpf]
	usuario_existe = lista_usuario_existente[0] if lista_usuario_existente else False
	return usuario_existe


## regra1: armazenar em lista
## regra2: formatos
##   cpf = 12345678911
##   nome = 
##   data_nascimento = dd/mm/aaaa
##   endereco = logradouro, no - bairro - cidade/uf
## regra3: verificar se o cpf/usuario já existe antes de cadastrar
def criar_usuario(lista_usuarios):
	print('\nInforme:')
	print('                       [ infome somente os números do CPF ]')
	cpf = input(' Número do CPF........: ').strip()
	usuario = verificar_usuario(lista_usuarios, cpf=cpf)

	if not usuario:
		print('                       [ nome completo ]')
		nome = input(
			' Nome do usuário......: ').upper()
		print('                       [ dd-mm-aaaa ]')
		data_nascimento = input(
			' Data de nascimento...: ')
		print('                       [ logradouro, número - bairro - cidade/uf ]')
		endereco = input(
			' Endereço.............: ').upper()
		lista_usuarios.append( {'cpf':cpf, 'nome':nome, 'data_nascimento':data_nascimento, 'endereco':endereco} )
		print('\nCPF cadastrado com sucesso!')
	else:
		print('\nCPF já cadastrado!')


# regra1: armazenar em lista
# regra2: formatos
#   agencia  ->  fixo = `0001`
#   conta_numero  ->  sequencial 1, 2, 3
#   usuario
## vincule um usuario a uma conta, filtre a lista de usuarios buscando o numero de cpf informado para cada usuario da lista
def criar_conta(agencia, conta_numero, lista_usuarios):
	print('\nInforme:')
	print('                       [ infome somente os números do CPF ]')
	cpf = input(' Número do CPF........: ').strip()
	usuario = verificar_usuario(lista_usuarios, cpf=cpf)
	
	if not usuario:
		print('\nCPF não cadastrado!')
	else:
		dados_conta = {'agencia':agencia, 'conta_numero':conta_numero, 'usuario':usuario}
		print('\nConta criada com sucesso!')
		return dados_conta


## regra1: deve receber argumentos apenas por posicao (argumentos: saldo, valor, extrato)
## regra2: retorno: saldo, extrato
def depositar(saldo, valor, extrato, /):
	# valor = float(input('Informe o valor do depósito: '))
	if valor > 0:
		saldo += valor
		extrato += f'Depósito: R$ {valor:.2f}\n'
	else:
		print('Operação falhou! O valor informado é inválido.')
	return saldo, extrato


## regra1: deve receber argumentos apenas por nome (argumentos: saldo, valor, extrato, limite, numero_saques, limite_saques)
## regra2: retorno: saldo, extrato
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
	# valor = float(input('Informe o valor do saque: '))
	excedeu_saldo = valor > saldo
	excedeu_limite = valor > limite
	excedeu_saques = numero_saques >= limite_saques

	if excedeu_saldo:		
		print('Operação falhou! Você não tem saldo suficiente.')
	elif excedeu_limite:	
		print('Operação falhou! O valor do saque excede o limite.')
	elif excedeu_saques:	
		print('Operação falhou! Número máximo de saques excedido.')
	elif valor > 0:
		saldo -= valor
		extrato += f'Saque: R$ {valor:.2f}\n'
		numero_saques += 1
	else:
		print('Operação falhou! O valor informado é inválido.')
	return saldo, extrato


## regra1: deve receber argumentos por posicao e nome (argumentos po posicao: saldo / argumentos nomeados: extrato)
def exibir_extrato(saldo, /, *, extrato):
	print('\n================ EXTRATO =================')
	print('Não foram realizadas movimentações.' if not extrato else extrato)
	print(f'\nSaldo: R$ {saldo:.2f}')
	print('==========================================')


def exibir_contas(lista_contas):
	for conta in lista_contas:
		print('==========================================')
		print(f' Agência...: {conta["agencia"]}')
		print(f' No. Conta.: {conta["conta_numero"]}')
		print(f' CPF.......: {conta["usuario"]["cpf"]}')
		print(f' Nome......: {conta["usuario"]["nome"]}')


def main():
	saldo = 0
	limite = 500
	extrato = ""
	numero_saques = 0
	LIMITE_SAQUES = 3
	AGENCIA = '0001'
	lista_usuarios = []
	lista_contas = []
	id_conta = 0
	menu = """

	[1] Depositar
	[2] Sacar
	[3] Extrato
	[4] Criar Usuário
	[5] Criar Conta Corrente
	[6] Listar Contas

	[0] Sair

	==> """

	while True:
		opcao = input(menu)

		## regra1: deixar codigo mais modular, criar funcoes para: sacar, depositar, extrato
		## regra2: criar 2 novas funcoes: criar_usuario, criar_conta (vinculada ao usuario)
		if opcao == '1':		
			valor = float(input('Informe o valor do depósito: '))
			saldo, extrato = depositar(saldo, valor, extrato)
		elif opcao == '2':
			valor = float(input('Informe o valor do saque: '))
			saldo, extrato = sacar(saldo=saldo, valor=valor, extrato=extrato, limite=limite, numero_saques=numero_saques, limite_saques=LIMITE_SAQUES)
		elif opcao == '3':	
			exibir_extrato(saldo, extrato=extrato)
		elif opcao == '4':	
			criar_usuario(lista_usuarios)
		elif opcao == '5':	
			id_conta += 1
			nova_conta = criar_conta(AGENCIA, id_conta, lista_usuarios)
			if nova_conta:
				lista_contas.append(nova_conta)
		elif opcao == '6':	
			exibir_contas(lista_contas)
		elif opcao == '0':
			break
		else:
			print('Operação inválida, por favor selecione novamente a operação desejada.')

main()
