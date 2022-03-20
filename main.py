"""
Início de tratamento de arquivo
"""

import time
import messagebox
import auxiliares as aux
import sys

# Processamento Paralelo 2
from pqdm.threads import pqdm

# from IPython.display import display  # pip install IPython

tupla = ('WE', 'Fornecedor: 234556 _345768_654556764_2343567_ R27')

print(aux.listarnumeros(tupla))

"""
#try:
tabela = 'GIG TESTE FORN'
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

for arquivo in aux.retornaarquivos(arquivo_caminho_origem):
    objarquivo = aux.TrabalhaArquivo(arquivo)
    inicioetapa = time.time()
    mensagemetapa = 'Verificando Cabeçalho...'
    print(mensagemetapa)

    objarquivo.verificacabecalho('|', quantcolunas, True)

    fimetapa = time.time()
    inicioetapa = aux.tratatempo(inicioetapa, fimetapa, mensagemetapa)
    mensagemetapa = 'Tratando Linha Quebrada...'
    print(mensagemetapa)
    linhascortadas, linhasacertadas = objarquivo.acertarlinhaquebrada('|')

    fimetapa = time.time()
    inicioetapa = aux.tratatempo(inicioetapa, fimetapa, mensagemetapa)
    mensagemetapa = 'Acertando Valor...'
    print(mensagemetapa)

    listadicionario = objarquivo.retornadf('Mont.em MI')

    # Processamento Paralelo 2
    fimetapa = time.time()
    inicioetapa = aux.tratatempo(inicioetapa, fimetapa, mensagemetapa)
    mensagemetapa = 'Preparando Carga de Fornecedor...'
    print(mensagemetapa)
    print('')
    dfcut = listadicionario[['Tipo', 'Texto']]
    argumentos = [tuple(x) for x in dfcut.to_numpy()]
    fimetapa = time.time()
    inicioetapa = aux.tratatempo(inicioetapa, fimetapa, mensagemetapa)
    mensagemetapa = 'Adicionando coluna Fornecedor...'
    print(mensagemetapa)
    listafornecedores = pqdm(argumentos, aux.listarnumeros, n_jobs=2, unit=' linhas')
    listadicionario['Fornecedores'] = listafornecedores

    fimetapa = time.time()
    inicioetapa = aux.tratatempo(inicioetapa, fimetapa, mensagemetapa)
    mensagemetapa = 'Salvando Arquivo...'
    print(mensagemetapa)

    print(listadicionario)

listadicionario.to_csv(arquivo_caminho_destino+'\\pandas.txt', index=None, sep='|', mode='a')

fimetapa = time.time()
inicioetapa = aux.tratatempo(inicioetapa, fimetapa, mensagemetapa)

tempofim = time.time()
tempototal = tempofim - tempoinicio

hours, rem = divmod(tempototal, 3600)
minutes, seconds = divmod(rem, 60)

messagebox.msgbox(
    f'O tempo decorrido foi de: {"{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), int(seconds))}',
    messagebox.MB_OK, 'Tempo Decorrido')

sys.exit()
"""