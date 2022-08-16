"""
Início de tratamento de arquivo
"""
import time
import messagebox
import auxiliares as aux
import sys
from pathlib import Path
import pandas as pd

# from IPython.display import display  # pip install IPython

# try:

codentrada = 'ANSI'  # 'UTF8'
tabela = 'GIG Entrada SAP com Fornecedor'
tabelafornecedor = 'GIG Texto Fornecedor'
listadicionario = None
listafornecedores = []

pergunta = messagebox.msgbox('Tem colunas de pré-cabeçalho?', messagebox.MB_YESNO,
                             'Tratamento de cabeçalho')
if pergunta == messagebox.IDYES:
    quantcolunas = int(messagebox.criarinputbox('Quant. colunas do arquivo', 'Quantas colunas tem o arquivo '
                                                                             '(lembrar que o SAP adiciona 2 colunas a '
                                                                             'mais)?'))
    if int(quantcolunas) < 4 or not str(quantcolunas).isnumeric():
        messagebox.msgbox('Valor inválido', messagebox.MB_OK, 'Valor inválido informado!')
        sys.exit()
else:
    quantcolunas = 0

tratarfornecedor = True
arquivo_caminho_origem = aux.caminhoselecionado(3, 'Arquivos a Tratar')
if len(arquivo_caminho_origem) == 0:
    messagebox.msgbox('Selecionar a pasta com os arquivos a serem tratados', messagebox.MB_OK,
                      'Caminho dos Arquivos a Tratar não selecionado')
    sys.exit()

resultado = 0

arquivo_caminho_destino = aux.caminhoselecionado(3, 'Lugar para Arquivos Tratados')
if len(arquivo_caminho_destino) == 0:
    messagebox.msgbox('Selecionar a pasta onde os arquivos tratados serão salvos', messagebox.MB_OK,
                      'Caminho Destino dos Arquivos Tratados não selecionado')
    sys.exit()

tempoinicio = time.time()

# Looping para "varrer" todos os arquivos da pasta (inclui os arquivos das subpastas)
mensagemetapa = ''

for arquivo in aux.retornaarquivos(arquivo_caminho_origem):
    objarquivo = aux.TrabalhaArquivo(arquivo)
    inicioetapa = time.time()
    mensagemetapa = 'Verificando Cabeçalho...'
    print(mensagemetapa)

    objarquivo.verificacabecalho('|', quantcolunas, True, codentrada)

    fimetapa = time.time()
    inicioetapa = aux.tratatempo(inicioetapa, fimetapa, mensagemetapa)
    mensagemetapa = 'Tratando Linha Quebrada...'
    print(mensagemetapa)
    linhascortadas, linhasacertadas = objarquivo.acertarlinhaquebrada('|', codificacao=codentrada)

    fimetapa = time.time()
    inicioetapa = aux.tratatempo(inicioetapa, fimetapa, mensagemetapa)
    mensagemetapa = 'Acertando Valor...'
    print(mensagemetapa)

    listadicionario = objarquivo.preparadf('Mont.em MI')
    # objarquivo.preparadf('Mont.em MI')

    fimetapa = time.time()
    inicioetapa = aux.tratatempo(inicioetapa, fimetapa, mensagemetapa)
    mensagemetapa = 'Salvando Arquivo Dados...'
    print(mensagemetapa)

    if listadicionario is not None:
        if not listadicionario.isEmpty():
            listadicionario.to_csv(arquivo_caminho_destino+'\\'+Path(arquivo).stem + '.txt', index=None, sep='|', mode='a', encoding=codentrada)

    # fimetapa = time.time()
    # inicioetapa = aux.tratatempo(inicioetapa, fimetapa, mensagemetapa)
    # mensagemetapa = 'Carregando dados para o banco...'
    # print(mensagemetapa)
    # aux.carregardf(tabela, listadicionario)

    fimetapa = time.time()
    inicioetapa = aux.tratatempo(inicioetapa, fimetapa, mensagemetapa)
    mensagemetapa = 'Salvando Arquivo Fornecedor/Material/Pedido...'
    print(mensagemetapa)

    if objarquivo.dadostexto is not None:
        if not objarquivo.dadostexto.dadosarquivo.isEmpty():
            objarquivo.dadostexto.to_csv(arquivo_caminho_destino + '\\' + Path(arquivo).stem + '_TextoQuebrado.txt', index=None, sep='|', mode='a', encoding=codentrada)

    # fimetapa = time.time()
    # inicioetapa = aux.tratatempo(inicioetapa, fimetapa, mensagemetapa)
    # mensagemetapa = 'Carregando fornecedores para o banco...'
    # print(mensagemetapa)
    # aux.carregardf(tabela, listafornecedores)


# del objarquivo.dadostexto
del objarquivo.dadostexto

fimetapa = time.time()
inicioetapa = aux.tratatempo(inicioetapa, fimetapa, mensagemetapa)

tempofim = time.time()
tempototal = tempofim - tempoinicio

hours, rem = divmod(tempototal, 3600)
minutes, seconds = divmod(rem, 60)

messagebox.msgbox(
    f'O tempo decorrido foi de: {"{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), int(seconds))}',
    messagebox.MB_OK, 'Tempo Decorrido')

# testar = aux.TrabalhaArquivo('c:\\teste\\teste.txt')
# print (testar.retornarinftexto('', 'NF:BXPED:1234567 INVOICE_FORN:179850', 'AJ', 'FORN', 6, 7))



