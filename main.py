import time
import messagebox
import auxiliares as aux
import os
import sys
import sensiveis as conf


quantcolunas = 0
tratarfornecedor = False
arquivo_caminho_origem = aux.caminhoselecionado(3)
if len(arquivo_caminho_origem) == 0:
    messagebox.msgbox('Selecionar a pasta com os arquivos a serem tratados', messagebox.MB_OK,
                      'Caminho dos Arquivos a Tratar não selecionado')
    sys.exit()

resultado = ''

arquivo_caminho_destino = aux.caminhoselecionado(3)
if len(arquivo_caminho_destino) == 0:
    messagebox.msgbox('Selecionar a pasta onde os arquivos tratados serão salvos', messagebox.MB_OK,
                      'Caminho Destino dos Arquivos Tratados não selecionado')
    sys.exit()


tempoinicio = time.time()


#Looping para "varrer" todos os arquivos da pasta (inclui os arquivos das subpastas)

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
    tabela = 'GIG OPEX Entrada Compromisso Ex Carga'
    if len(caminhofornec) > 0:
        caminhoerrofornec = caminhofornec.upper()
        caminhoerrofornec = caminhoerrofornec.replace('.TXT', '.ERR')
        caminhologfornec = caminhofornec.upper()
        caminhologfornec = caminhologfornec.replace('.TXT', '.LOG')
        tabelafornecedor = 'GIG IndicexFornecedor'
    tempopergunta = time.time()
    if resultado == '':
        resultado = messagebox.msgbox('Subir pro banco?', messagebox.MB_YESNO, 'Carga SQL')
    temporesposta = time.time()
    if resultado == messagebox.IDYES:
        os.system('bcp ' + conf.schema + '."[' + tabela + ']" IN "' + caminhosalvo + '" -t "|" -C SQL_Latin1_General_CP1_CI_AS -c -S ' + conf.endbanco + ' -U ' + conf.usrbanco + ' -P ' + conf.pwdbanco + ' -d ' + conf.nomebanco + ' -e "' + caminhoerro + '" -F 2 > "' + caminholog+'"')
        if len(caminhofornec) > 0:
            os.system('bcp ' + conf.schema + '."[' + tabelafornecedor + ']" IN ' + caminhofornec + ' -t "|" -C SQL_Latin1_General_CP1_CI_AS -c -S ' + conf.endbanco + ' -U ' + conf.usrbanco + ' -P ' + conf.pwdbanco + ' -d ' + conf.nomebanco + ' -e ' + caminhoerrofornec + ' -F 2 > ' + caminhologfornec)


tempofim = time.time()

if tratarfornecedor:
    tempototal = (tempopergunta-tempoinicio)+(tempofim-temporesposta)
else:
    tempototal = tempofim - tempoinicio

hours, rem = divmod(tempototal, 3600)
minutes, seconds = divmod(rem, 60)

messagebox.msgbox(f'O tempo decorrido foi de: {"{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), int(seconds))}', messagebox.MB_OK, 'Tempo Decorrido')
