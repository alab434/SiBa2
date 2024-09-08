import os


def limpar_tela():
	if os.name == 'posix':  # Linux ou macOS
		os.system('clear')
	elif os.name == 'nt':  # Windows
		os.system('cls')


def menu_titulo():
	limpar_tela()
	print('\n' + ' BANCO PRAÇA '.center(MENU_LARGURA, '$') + '\n')


def menu_subtitulo(texto):
	print(f' {texto.upper()} '.center(MENU_LARGURA, '_') + '\n')


def menu_fim():
	print(MENU_LARGURA*'_')


def menu_opcoes():
	MENU_OPCOES = f'''{' MENU '.center(MENU_LARGURA, '_')}
   
   [1] VISUALIZAR EXTRATO      [4] CRIAR USUÁRIO
   [2] DEPOSITAR               [5] CRIAR CONTA
   [3] SACAR                   [6] EXIBIR CONTAS

   [0] SAIR
{MENU_LARGURA*'_'}

>> ESCOLHA UMA OPÇÃO: '''
	return int(input(MENU_OPCOES))


# def calcular_saldo(valores):
# 	valor_saldo = 0.00
# 	for item in conta_extrato_historico:
# 		valor_saldo += -item[1] if item[0] == 'SAQUE' else item[1]
# 	return valor_saldo


## regra1: deve receber argumentos por posicao e nome (argumentos po posicao: saldo / argumentos nomeados: extrato)
def extrato(saldo, /, *, extrato):
	voltar = -99
	# saldo_disponivel = calcular_saldo(extrato)

	while voltar != 0:
		menu_titulo()
		menu_subtitulo('EXTRATO')

		for item in extrato:
			simbolo = '-' if item[0] == 'SAQUE' else '+'
			print(f'   {item[0]:20} {simbolo} R$ {item[1]:9.2f}')
		
		print(32*' -')
		print(f'   SALDO DISPONÍVEL     = R$ {saldo:9.2f}')

		print(MENU_LARGURA*'_')
		voltar = int(input(MENU_VOLTAR_MENSAGEM))
	

## regra1: deve receber argumentos apenas por posicao (argumentos: saldo, valor, extrato)
## regra2: retorno: saldo, extrato
def depositar(saldo, valor_deposito, extrato, /):
	voltar = -99

	while voltar != 0:
		menu_titulo()
		menu_subtitulo('DEPÓSITO')

		# valor_deposito = float(input('>> QUAL O VALOR DE DEPÓSITO? '))
		if valor_deposito <= 0:
			print(32*' -','\n')
			print(f'>> OPERAÇÃO NÃO REALIZADA!')
			print(f'   VALOR INVÁLIDO.')
		else:
			extrato.append(('DEPOSITO', valor_deposito))
			saldo += valor_deposito
			print(32*' -','\n')
			print(f'>> OPERAÇÃO REALIZADA COM SUCESSO!')
			print(f'   DEPÓSITO EFETUADO      R$ {valor_deposito:9.2f}')

		print(MENU_LARGURA*'_')
		voltar = int(input(MENU_VOLTAR_MENSAGEM))
	return saldo, extrato


## regra1: deve receber argumentos apenas por nome (argumentos: saldo, valor, extrato, limite, numero_saques, limite_saques)
## regra2: retorno: saldo, extrato
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
	voltar = -99
	# saldo_disponivel = calcular_saldo(conta_extrato_historico)
	# global saques_efetuados_dia
	# global saques_valor_total_dia

	while voltar != 0:
		menu_titulo()
		menu_subtitulo('SAQUE')

		if saldo <= 0.00:
			print(32*' -','\n')
			print(f'>> OPERAÇÃO NÃO REALIZADA!')
			print(f'   A CONTA NÃO POSSUE SALDO.')
		elif numero_saques >= limite_saques:
			print(32*' -','\n')
			print(f'>> OPERAÇÃO NÃO REALIZADA!')
			print(f'   LIMITE DE SAQUES DIÁRIO ATINGIDO.')
		else:
			print(f'   SALDO DISPONÍVEL     = R$ {saldo:9.2f}')
			print(MENU_LARGURA*'_')
			# valor_saque = float(input('\n>> QUAL O VALOR DO SAQUE? '))

			if valor <= 0:
				print(32*' -','\n')
				print(f'>> OPERAÇÃO NÃO REALIZADA!')
				print(f'   VALOR INVÁLIDO.')
			else:
				if valor > saldo:
					print(32*' -','\n')
					print(f'>> OPERAÇÃO NÃO REALIZADA!')
					print(f'   SALDO INSUFICIENTE.')
				elif valor > limite:
					print(32*' -','\n')
					print(f'>> OPERAÇÃO NÃO REALIZADA!')
					print(f'   O VALOR MÁXIMO PARA SAQUES É R$ {limite}')
				else:
					extrato.append(('SAQUE', valor))
					saldo -= valor
					# saques_valor_total_dia += valor
					numero_saques += 1
					print(32*' -','\n')
					print(f'>> OPERAÇÃO REALIZADA COM SUCESSO!')
					print(f'   SAQUE EFETUADO         R$ {valor:9.2f}')
				
		print(MENU_LARGURA*'_')
		voltar = int(input(MENU_VOLTAR_MENSAGEM))
	
	return saldo, extrato, numero_saques


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
	voltar = -99

	while voltar != 0:
		menu_titulo()
		menu_subtitulo('CRIAR USUÁRIO')	
		print('                      * somente os números')
		cpf = input(' NÚMERO DO CPF......: ').strip()
		usuario = verificar_usuario(lista_usuarios, cpf=cpf)

		if not usuario:
			print('                      * nome completo ')
			nome = input(
				' NOME DO USUÁRIO....: ').upper()
			print('                      * dd-mm-aaaa ')
			data_nascimento = input(
				' DATA DE NASCIMENTO.: ')
			print('                      * logradouro, número - bairro - cidade/uf ')
			endereco = input(
				' ENDEREÇO...........: ').upper()
			lista_usuarios.append( {'cpf':cpf, 'nome':nome, 'data_nascimento':data_nascimento, 'endereco':endereco} )
			print(32*' -','\n')
			print(f'>> OPERAÇÃO REALIZADA COM SUCESSO!')
			print(f'   USUARIO CADASTRADO.')
		else:
			print(32*' -','\n')
			print(f'>> OPERAÇÃO NÃO REALIZADA!')
			print(f'   CPF JÁ CADASTRADO.')
		
		print(MENU_LARGURA*'_')
		voltar = int(input(MENU_VOLTAR_MENSAGEM))


# regra1: armazenar em lista
# regra2: formatos
#   agencia  ->  fixo = `0001`
#   conta_numero  ->  sequencial 1, 2, 3
#   usuario
## vincule um usuario a uma conta, filtre a lista de usuarios buscando o numero de cpf informado para cada usuario da lista
def criar_conta(agencia, conta_numero, lista_usuarios):
	voltar = -99

	while voltar != 0:
		menu_titulo()
		menu_subtitulo('CRIAR CONTA')	
		print('                      * somente os números')
		cpf = input(' NÚMERO DO CPF......: ').strip()
		usuario = verificar_usuario(lista_usuarios, cpf=cpf)
		
		if not usuario:
			print(32*' -','\n')
			print(f'>> OPERAÇÃO NÃO REALIZADA!')
			print(f'   CPF NÃO CADASTRADO.')
			print(MENU_LARGURA*'_')
			voltar = int(input(MENU_VOLTAR_MENSAGEM))
		else:
			dados_conta = {'agencia':agencia, 'conta_numero':conta_numero, 'usuario':usuario}
			print(32*' -','\n')
			print(f'>> OPERAÇÃO REALIZADA COM SUCESSO!')
			print(f'   CONTA CRIADA.')
			print(MENU_LARGURA*'_')
			voltar = int(input(MENU_VOLTAR_MENSAGEM))
			return dados_conta


def exibir_contas(lista_contas):
	voltar = -99

	while voltar != 0:
		menu_titulo()
		menu_subtitulo('EXIBIR CONTAS')	
		for conta in lista_contas:
			print(32*' -','\n')
			print(f' AGÊNCIA...: {conta["agencia"]}')
			print(f' NO. CONTA.: {conta["conta_numero"]}')
			print(f' CPF.......: {conta["usuario"]["cpf"]}')
			print(f' NOME......: {conta["usuario"]["nome"]}')
		print(MENU_LARGURA*'_')
		voltar = int(input(MENU_VOLTAR_MENSAGEM))

## *******************************************************************
"""
	Sistema Bancário Simples:
	- EXTRATO
	- DEPOSITO
	- SAQUE
	- CRIAR USUARIO
	- CRIAR CONTA
	- LISTAR CONTAS
"""
MENU_LARGURA = 64
MENU_VOLTAR_MENSAGEM = '\n>> TECLE [0] PARA VOLTAR AO MENU: '

def main():
	AGENCIA = '0001'
	SAQUES_VALOR_LIMITE_POR_TRANSACAO = 500.00
	SAQUES_QUANTIDADE_POR_DIA = 3
	# saques_valor_total_dia = 0.00
	opcao_escolhida = -99
	numero_saques = 0
	id_conta = 0
	saldo = 0
	conta_extrato_historico = [] # extrato = ''
	lista_usuarios = []
	lista_contas = []

	while opcao_escolhida != 0:
		menu_titulo()
		opcao_escolhida = menu_opcoes()
		"""
			[1] VISUALIZAR EXTRATO      [4] CRIAR USUÁRIO
			[2] DEPOSITAR               [5] CRIAR CONTA
			[3] SACAR                   [6] EXIBIR CONTAS
		"""
		if opcao_escolhida == 1:
			extrato(saldo, extrato=conta_extrato_historico)
		elif opcao_escolhida == 2:
			valor_deposito = float(input('>> QUAL O VALOR DE DEPÓSITO? '))
			saldo, conta_extrato_historico = depositar(saldo, valor_deposito, conta_extrato_historico)
		elif opcao_escolhida == 3:
			valor_saque = float(input('\n>> QUAL O VALOR DO SAQUE? '))
			saldo, conta_extrato_historico, numero_saques = sacar(saldo=saldo, valor=valor_saque, extrato=conta_extrato_historico, limite=SAQUES_VALOR_LIMITE_POR_TRANSACAO, numero_saques=numero_saques, limite_saques=SAQUES_QUANTIDADE_POR_DIA)
		elif opcao_escolhida == 4:
			novo_usuario = criar_usuario(lista_usuarios)
		elif opcao_escolhida == 5:
			id_conta += 1 
			nova_conta = criar_conta(AGENCIA, id_conta, lista_usuarios)
			if nova_conta:
				lista_contas.append(nova_conta)
		elif opcao_escolhida == 6:
			exibir_contas(lista_contas)
	else:
		menu_fim()
		print()
		menu_titulo()
		print(f' FIM DO ATENDIMENTO '.center(MENU_LARGURA, '_'))
		print(3*'\n')


main()
