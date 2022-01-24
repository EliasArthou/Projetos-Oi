"""
Início de tratamento de arquivo
"""

import time
import messagebox
import auxiliares as aux
import os
import sys
import sensiveis as conf


tabela = ''
tabelafornecedor = ''


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

tratarfornecedor = False
arquivo_caminho_origem = aux.caminhoselecionado(3)
if len(arquivo_caminho_origem) == 0:
    messagebox.msgbox('Selecionar a pasta com os arquivos a serem tratados', messagebox.MB_OK,
                      'Caminho dos Arquivos a Tratar não selecionado')
    sys.exit()

resultado = 0

arquivo_caminho_destino = aux.caminhoselecionado(3)
if len(arquivo_caminho_destino) == 0:
    messagebox.msgbox('Selecionar a pasta onde os arquivos tratados serão salvos', messagebox.MB_OK,
                      'Caminho Destino dos Arquivos Tratados não selecionado')
    sys.exit()

tempoinicio = time.time()

# Looping para "varrer" todos os arquivos da pasta (inclui os arquivos das subpastas)

for arquivo in aux.retornaarquivos(arquivo_caminho_origem):
    objarquivo = aux.TrabalhaArquivo(arquivo)
    objarquivo.verificacabecalho('|', quantcolunas)
    linhascortadas, linhasacertadas = objarquivo.acertarlinhaquebrada('|')

    caminhosalvo, caminhofornec = objarquivo.salvar_arquivo(arquivo_caminho_destino, tratarfornecedor)

    caminhoerro = caminhosalvo.upper()
    caminhoerro = caminhoerro.replace('.TXT', '.ERR')
    caminholog = caminhosalvo.upper()
    caminholog = caminholog.replace('.TXT', '.LOG')
    tempopergunta = time.time()
    # [GIG Analise Compromisso]

    # tabela = 'GIG OPEX Entrada Compromisso Ex Carga'
    if len(caminhofornec) > 0:
        caminhoerrofornec = caminhofornec.upper()
        caminhoerrofornec = caminhoerrofornec.replace('.TXT', '.ERR')
        caminhologfornec = caminhofornec.upper()
        caminhologfornec = caminhologfornec.replace('.TXT', '.LOG')
        tabelafornecedor = 'GIG IndicexFornecedor'
    tempopergunta = time.time()
    if resultado == 0:
        resultado = messagebox.msgbox('Subir pro banco?', messagebox.MB_YESNO, 'Carga SQL')
    temporesposta = time.time()
    if resultado == messagebox.IDYES:
        if len(tabela) == 0:
            tabela = messagebox.criarinputbox('Tabela Banco', 'Digite a tabela a ser carregada:')

        if len(tabela) > 0:
            # Posterior criação de verificação de quantidade de campos e se a tabela existe
            # (posso criar uma verificação de tipos dos campos também)
            if len(caminhofornec) > 0:
                tabelafornecedor = messagebox.criarinputbox('Tabela Banco',
                                                            'Digite a tabela de fornecedor a ser carregada:')

            if len(tabela) > 0 and ((len(caminhofornec) > 0 and len(tabelafornecedor) > 0) or len(caminhofornec) == 0):
                os.system('bcp ' + conf.schema + '."[' + tabela + ']" IN "'
                          + caminhosalvo + '" -t "|" -C SQL_Latin1_General_CP1_CI_AS -c -S ' +
                          conf.endbanco + ' -U ' + conf.usrbanco + ' -P ' + conf.pwdbanco + ' -d '
                          + conf.nomebanco + ' -e "' + caminhoerro + '" -F 2 > "' + caminholog + '"')
                if len(caminhofornec) > 0:
                    os.system('bcp ' + conf.schema + '."[' + tabelafornecedor + ']" IN ' + caminhofornec +
                              ' -t "|" -C SQL_Latin1_General_CP1_CI_AS -c -S ' + conf.endbanco + ' -U ' +
                              conf.usrbanco + ' -P ' + conf.pwdbanco + ' -d ' + conf.nomebanco + ' -e ' +
                              caminhoerrofornec + ' -F 2 > ' + caminhologfornec)
        else:
            messagebox.msgbox('Valor inválido', messagebox.MB_OK, 'Nome da tabela não informado!')
            sys.exit()

tempofim = time.time()

if tratarfornecedor:
    tempototal = (tempopergunta - tempoinicio) + (tempofim - temporesposta)
else:
    tempototal = tempofim - tempoinicio

hours, rem = divmod(tempototal, 3600)
minutes, seconds = divmod(rem, 60)

messagebox.msgbox(
    f'O tempo decorrido foi de: {"{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), int(seconds))}',
    messagebox.MB_OK, 'Tempo Decorrido')
