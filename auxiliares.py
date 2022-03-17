"""
Funções Auxiliares
"""
import os.path
import re
import pandas as pd
import time
from tqdm import tqdm

import pypyodbc

import messagebox
import sensiveis as pwd


def caminhospadroes(caminho):
    """

    :param caminho: opção do caminho padrão que gostaria de retornar (em caso de dúvida ver lista abaixo).
    :return: o caminho segundo a opção dada como entrada.
    """
    import ctypes.wintypes
    # CSIDL	                        Decimal	Hex	    Shell	Description
    # CSIDL_ADMINTOOLS	            48	    0x30	5.0	    The file system directory that is used to store administrative tools for an individual user.
    # CSIDL_ALTSTARTUP	            29	    0x1D	 	    The file system directory that corresponds to the user's nonlocalized Startup program group.
    # CSIDL_APPDATA	                26	    0x1A	4.71	The file system directory that serves as a common repository for application-specific data.
    # CSIDL_BITBUCKET	            10	    0x0A	 	    The virtual folder containing the objects in the user's Recycle Bin.
    # CSIDL_CDBURN_AREA	            59	    0x3B	6.0	    The file system directory acting as a staging area for files waiting to be written to CD.
    # CSIDL_COMMON_ADMINTOOLS	    47	    0x2F	5.0	    The file system directory containing administrative tools for all users of the computer.
    # CSIDL_COMMON_ALTSTARTUP	    30	    0x1E	        NT-based only	The file system directory that corresponds to the nonlocalized Startup program group for all users.
    # CSIDL_COMMON_APPDATA	        35	    0x23	5.0	    The file system directory containing application data for all users.
    # CSIDL_COMMON_DESKTOPDIRECTORY	25	    0x19	        NT-based only	The file system directory that contains files and folders that appear on the desktop for all users.
    # CSIDL_COMMON_DOCUMENTS	    46	    0x2E	 	    The file system directory that contains documents that are common to all users.
    # CSIDL_COMMON_FAVORITES	    31	    0x1F	        NT-based only	The file system directory that serves as a common repository for favorite items common to all users.
    # CSIDL_COMMON_MUSIC	        53	    0x35	6.0	    The file system directory that serves as a repository for music files common to all users.
    # CSIDL_COMMON_PICTURES	        54	    0x36	6.0	    The file system directory that serves as a repository for image files common to all users.
    # CSIDL_COMMON_PROGRAMS	        23	    0x17	        NT-based only	The file system directory that contains the directories for the common program groups that appear on the Start menu for all users.
    # CSIDL_COMMON_STARTMENU	    22	    0x16	        NT-based only	The file system directory that contains the programs and folders that appear on the Start menu for all users.
    # CSIDL_COMMON_STARTUP	        24	    0x18	        NT-based only	The file system directory that contains the programs that appear in the Startup folder for all users.
    # CSIDL_COMMON_TEMPLATES	    45	    0x2D	        NT-based only	The file system directory that contains the templates that are available to all users.
    # CSIDL_COMMON_VIDEO	        55	    0x37	6.0	    The file system directory that serves as a repository for video files common to all users.
    # CSIDL_COMPUTERSNEARME	        61	    0x3D	6.0	    The folder representing other machines in your workgroup.
    # CSIDL_CONNECTIONS	            49	    0x31	6.0	    The virtual folder representing Network Connections, containing network and dial-up connections.
    # CSIDL_CONTROLS	            3	    0x03	 	    The virtual folder containing icons for the Control Panel applications.
    # CSIDL_COOKIES	                33	    0x21	 	    The file system directory that serves as a common repository for Internet cookies.
    # CSIDL_DESKTOP	                0	    0x00	 	    The virtual folder representing the Windows desktop, the root of the shell namespace.
    # CSIDL_DESKTOPDIRECTORY	    16	    0x10	 	    The file system directory used to physically store file objects on the desktop.
    # CSIDL_DRIVES	                17	    0x11	 	    The virtual folder representing My Computer, containing everything on the local computer: storage devices, printers, and Control Panel. The folder may also contain mapped network drives.
    # CSIDL_FAVORITES	            6	    0x06	 	    The file system directory that serves as a common repository for the user's favorite items.
    # CSIDL_FONTS	                20	    0x14	 	    A virtual folder containing fonts.
    # CSIDL_HISTORY	                34	    0x22	 	    The file system directory that serves as a common repository for Internet history items.
    # CSIDL_INTERNET	            1	    0x01	 	    A viritual folder for Internet Explorer.
    # CSIDL_INTERNET_CACHE	        32	    0x20	4.72	The file system directory that serves as a common repository for temporary Internet files.
    # CSIDL_LOCAL_APPDATA	        28	    0x1C	5.0	    The file system directory that serves as a data repository for local (nonroaming) applications.
    # CSIDL_MYDOCUMENTS	            5	    0x05	6.0	    The virtual folder representing the My Documents desktop item.
    # CSIDL_MYMUSIC	                13	    0x0D	6.0	    The file system directory that serves as a common repository for music files.
    # CSIDL_MYPICTURES	            39	    0x27	5.0	    The file system directory that serves as a common repository for image files.
    # CSIDL_MYVIDEO	                14	    0x0E	6.0	    The file system directory that serves as a common repository for video files.
    # CSIDL_NETHOOD	                19	    0x13	 	    A file system directory containing the link objects that may exist in the My Network Places virtual folder.
    # CSIDL_NETWORK	                18	    0x12	 	    A virtual folder representing Network Neighborhood, the root of the network namespace hierarchy.
    # CSIDL_PERSONAL	            5	    0x05	 	    The file system directory used to physically store a user's common repository of documents. (From shell version 6.0 onwards, CSIDL_PERSONAL is equivalent to CSIDL_MYDOCUMENTS, which is a virtual folder.)
    # CSIDL_PHOTOALBUMS	            69	    0x45	Vista	The virtual folder used to store photo albums.
    # CSIDL_PLAYLISTS	            63	    0x3F	Vista	The virtual folder used to store play albums.
    # CSIDL_PRINTERS	            4	    0x04	 	    The virtual folder containing installed printers.
    # CSIDL_PRINTHOOD	            27	    0x1B	 	    The file system directory that contains the link objects that can exist in the Printers virtual folder.
    # CSIDL_PROFILE	                40	    0x28	5.0	    The user's profile folder.
    # CSIDL_PROGRAM_FILES	        38	    0x26	5.0	    The Program Files folder.
    # CSIDL_PROGRAM_FILESX86	    42	    0x2A	5.0	    The Program Files folder for 32-bit programs on 64-bit systems.
    # CSIDL_PROGRAM_FILES_COMMON	43	    0x2B	5.0	    A folder for components that are shared across applications.
    # CSIDL_PROGRAM_FILES_COMMONX86	44	    0x2C	5.0	    A folder for 32-bit components that are shared across applications on 64-bit systems.
    # CSIDL_PROGRAMS	            2	    0x02	 	    The file system directory that contains the user's program groups (which are themselves file system directories).
    # CSIDL_RECENT	                8	    0x08	 	    The file system directory that contains shortcuts to the user's most recently used documents.
    # CSIDL_RESOURCES	            56	    0x38	6.0	    The file system directory that contains resource data.
    # CSIDL_RESOURCES_LOCALIZED	    57	    0x39	6.0	    The file system directory that contains localized resource data.
    # CSIDL_SAMPLE_MUSIC	        64	    0x40	Vista	The file system directory that contains sample music.
    # CSIDL_SAMPLE_PLAYLISTS	    65	    0x41	Vista	The file system directory that contains sample playlists.
    # CSIDL_SAMPLE_PICTURES	        66	    0x42	Vista	The file system directory that contains sample pictures.
    # CSIDL_SAMPLE_VIDEOS	        67	    0x43	Vista	The file system directory that contains sample videos.
    # CSIDL_SENDTO	                9	    0x09	 	    The file system directory that contains Send To menu items.
    # CSIDL_STARTMENU	            11	    0x0B	 	    The file system directory containing Start menu items.
    # CSIDL_STARTUP	                7	    0x07	 	    The file system directory that corresponds to the user's Startup program group.
    # CSIDL_SYSTEM	                37	    0x25	5.0	    The Windows System folder.
    # CSIDL_SYSTEMX86	            41	    0x29	5.0	    The Windows 32-bit System folder on 64-bit systems.
    # CSIDL_TEMPLATES	            21	    0x15	 	    The file system directory that serves as a common repository for document templates.
    # CSIDL_WINDOWS	                36	    0x24	5.0	    The Windows directory or SYSROOT.

    csidl_personal = caminho  # Caminho padrão
    shgfp_type_current = 0  # Para não pegar a pasta padrão e sim a definida como documentos

    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.Shell32.SHGetFolderPathW(None, csidl_personal, None, shgfp_type_current, buf)

    return buf.value


def caminhoselecionado(tipojanela=1, titulo=''):
    """
    :param tipojanela: tipo de dialog
    :param titulo: Título da Janela
    :return:
    """
    import tkinter as tk
    from tkinter import filedialog

    'Cria a janela raiz'
    root = tk.Tk()
    root.withdraw()

    if tipojanela == 1:
        retorno = filedialog.askopenfilename(title='Selecione o arquivo a ser tratado:',
                                             initialdir=caminhospadroes(5), filetypes=[('Arquivos Texto', '*.txt')])
        if retorno is None:  # asksaveasfile return `None` if dialog closed with "cancel".
            return ''

    elif tipojanela == 2:
        name = filedialog.asksaveasfile(mode='w', defaultextension='.txt',
                                        filetypes=(('Arquivos Texto', '*.txt'), ('Todos os Arquivos', '*.*')),
                                        initialdir=caminhospadroes(5),
                                        title='Selecione onde salvar o arquivo')
        if name is None:  # asksaveasfile return `None` if dialog closed with "cancel".
            return ''
        text2save = str(name.name)
        name.write('')
        retorno = text2save

    elif tipojanela == 3:
        name = filedialog.askdirectory(initialdir=caminhospadroes(5), title=titulo)
        if name is None:  # askdirectory return `None` if dialog closed with "cancel".
            return ''
        text2save = name
        retorno = text2save

    else:
        return

    return retorno


def retornaarquivos(caminho):
    """

    :param caminho: caminho dos arquivos para ser listado.
    :return:
    """
    import os

    lista = []

    if len(caminho) > 0:
        for diretorio, subpastas, arquivos in os.walk(caminho):
            for arquivo in arquivos:
                arquivoatual = os.path.join(os.path.realpath(diretorio), arquivo)
                if right(arquivoatual.upper(), 4) == '.TXT':  # Equivalente a 4 dígitos a direita
                    lista.append(os.path.join(os.path.realpath(diretorio), arquivo))
    else:
        return

    return lista


def left(s, amount):
    """

    :param s: string a ser tratada.
    :param amount: quantidade de caracteres a esquerda.
    :return:
    """
    return s[:amount]


def right(s, amount):
    """

    :param s: string a ser tratada.
    :param amount: quantidade de caracteres a direita.
    :return:
    """
    return s[-amount:]


def mid(s, offset, amount):
    """
    :param s: string a ser tratada.
    :param offset: caracter de início.
    :param amount: quantidade de caracteres.
    :return:
    """
    return s[(offset - 1):(offset - 1) + amount]


def index_of(val, in_list):
    """
    :param val: valor a ser procurado.
    :param in_list: lista a ser efetuada a busca.
    :return:
    """
    try:
        return in_list.index(val)
    except ValueError:
        return -1


def listarnumeros(tipo, texto, transformaremtexto=False):
    """
    :param transformaremtexto: transformar a lista em texto.
    :param tipo: tipo do lançamento.
    :param texto: texto para extrair os números.
    :return:
    """
    tipo = tipo.strip()

    texto = texto.strip()

    match tipo:
        case 'WE' | 'AB' | 'D6' | 'RE':
            lista = re.findall(r'Forn[\D*]*([\d]+)[\D]', texto)

        case 'EP' | 'PV':
            lista = re.findall(r'_([\d]{6,7})_', texto)

        case _:
            lista = re.findall(r'([\d]{6,7}[\d]*)[\D]', texto)

    # Verifica se achou números segundo as regras definidas
    if len(lista) > 0:
        # Tira o espaço dos números encontrados no campo
        lista = [linha.strip() for linha in lista]
        # Tira as duplicatas (caso tenha)
        lista = list(set(lista))

    if transformaremtexto:
        listatemp = lista
        lista = ', '
        lista = lista.join(listatemp)

    return lista


class TrabalhaArquivo:
    """
    Classe para tratamento de arquivo.
    """
    def __init__(self, caminho):
        self.caminho = caminho
        self.precabecalho = []
        self.listaarquivo = []
        self.quantidadelinhas = []
        self.cabecalho = ''
        self.quantcampos = 0
        self.separador = ''
        self.cabecalhooriginal = ''

    def retornaindice(self, textocabecalho):
        """
        :param textocabecalho: texto do índice a ser procurado.
        :return:
        """
        if len(self.cabecalho) != 0:
            if type(self.cabecalho) is list:
                indice = index_of(textocabecalho, self.cabecalho)
            else:
                indice = index_of(textocabecalho, self.cabecalho.split(self.separador))

            return indice
        else:
            return -1

    def verificacabecalho(self, separador, quantcampos=0, quebracabecalho=False, adicionafornecedor=False):
        """
        :param adicionafornecedor: se adiciona o campo fornecedor no cabeçalho.
        :param separador: caracter de separação.
        :param quantcampos: quantidade de campos.
        :param quebracabecalho: se o cabeçalho desse ser lista ou "string".
        """

        if len(self.separador) == 0:
            self.separador = separador

        with open(self.caminho, 'r', encoding='ANSI') as arquivo:
            texto = arquivo.readlines()
            for linha in texto:
                linha = linha.strip()
                if (left(linha, 1) == separador and right(linha, 1) == separador and quantcampos == 0) or \
                        len(linha.split(separador)) == quantcampos:
                    self.cabecalhooriginal = linha
                    if adicionafornecedor:
                        linha = left(linha, len(linha)-1) + separador + 'Fornecedores' + separador
                    self.quantcampos = len(linha.split(separador))
                    cabecalhoacertado = [campo.strip() for campo in linha.split(separador)]

                    if quebracabecalho:
                        self.cabecalho = cabecalhoacertado
                    else:
                        self.cabecalho = separador.join([campo for campo in self.cabecalho])
                    break

                else:
                    self.precabecalho.append(linha)

    def acertarlinhaquebrada(self, separador='', adicionacabecalho=True, adicionafornecedores=False):
        """
        :param adicionafornecedores: se precisa adicionar o campo de fornecedores (e ele será tratado)
        :param separador: campo de separação.
        :param adicionacabecalho: se deve incluir o cabeçalho ou não.
        :return:
        """
        try:
            linhaanterior = ''
            listalinhascortadas = []
            listalinhasacertadas = []

            if len(self.separador) > 0:
                separadorlocal = self.separador
            else:
                separadorlocal = separador
            if self.quantcampos > 0:
                if adicionacabecalho:
                    if type(self.cabecalho) is not list:
                        self.listaarquivo.append(self.cabecalho.split(separadorlocal))
                    else:
                        cabecalholocal = separadorlocal.join([campo for campo in self.cabecalho])
                        self.listaarquivo.append(cabecalholocal)

                quantidadelinhasarquivo = self.contarlinhasarq()
                self.quantidadelinhas.append(quantidadelinhasarquivo)

                with open(self.caminho, 'r', encoding='ANSI') as arquivo:
                    texto = arquivo.readlines()
                    with tqdm(total=quantidadelinhasarquivo) as barra_progresso:
                        for linha in texto:
                            linhaparaadicionar = []
                            linha = linha.strip()
                            barra_progresso.update()
                            time.sleep(1)
                            if index_of(linha.replace('|', ''), self.precabecalho) == -1 and linha != self.cabecalhooriginal \
                                    and linha.split(self.separador) != self.cabecalhooriginal:
                                if linha.replace(self.separador, '') != '-' * len(linha.replace(self.separador, '')) and mid(
                                        linha.replace(' ', ''), 2, 1) != '*':
                                    if (len(linha.split(separadorlocal)) < self.quantcampos and not adicionafornecedores) \
                                            or (len(linha.split(separadorlocal)) < self.quantcampos-1 and adicionafornecedores):
                                        if len(linhaanterior) > 0:
                                            novalinha = linhaanterior + linha

                                        if linhaanterior == '':
                                            linhaanterior = linha

                                        elif len(novalinha.split(separadorlocal)) > self.quantcampos:
                                            linhaanterior = ''
                                            novalinha = ''

                                        elif len(novalinha.split(separadorlocal)) == self.quantcampos:
                                            listalinhascortadas.append(linhaanterior.split(separadorlocal))
                                            listalinhascortadas.append(linha.split(separadorlocal))
                                            listalinhasacertadas.append(novalinha.split(separadorlocal))
                                            linhaparaadicionar = novalinha.split(separadorlocal)
                                            novalinha = ''
                                            linhaanterior = ''
                                    else:
                                        if len(linha.split(separadorlocal)) == self.quantcampos:
                                            novalinha = ''
                                            linhaanterior = ''
                                        else:
                                            camposamais = len(linha.split(separadorlocal)) - self.quantcampos
                                            linhainvertida = linha[::-1]
                                            linhainvertida = mid(linhainvertida, 2, len(linhainvertida) - 1)

                                            for campos in range(camposamais):
                                                if separadorlocal != '\t':
                                                    linhainvertida = linhainvertida.replace(separadorlocal, '\t', 1)
                                                else:
                                                    linhainvertida = linhainvertida.replace(separadorlocal, '|', 1)

                                            linhainvertida = '|' + linhainvertida
                                            linha = linhainvertida[::-1]
                                        linhaparaadicionar = linha.split(separadorlocal)
                                    if adicionafornecedores:
                                        if self.retornaindice('Tipo') != -1 and self.retornaindice('Texto') != -1:
                                            print(linhaparaadicionar[self.retornaindice('Tipo')], linhaparaadicionar[self.retornaindice('Texto')])
                                            linhaparaadicionar['Fornecedores'] = listarnumeros(linhaparaadicionar[self.retornaindice('Tipo')],
                                                                                               linhaparaadicionar[self.retornaindice('Texto')])
                                    self.listaarquivo.append(linhaparaadicionar)

                    return listalinhascortadas, listalinhasacertadas
        except Exception as e:
            messagebox.msgbox(str(e)+chr(13)+'Linha: ' + linha, messagebox.MB_OK, 'Erro')

    def contarlinhasarq(self):
        quantlinha = 0
        with open(self.caminho, 'r', encoding='ANSI') as arquivo:
            texto = arquivo.readlines()
            for linha in texto:
                quantlinha += 1

        return quantlinha

    def salvar_arquivo(self, destino):
        """
        :param destino: caminho de destino dos arquivos.
        :param tratarfornecedor: se tem que fazer o arquivo de fornecedor ou não.
        :return:
        """
        linhatemp = ''
        caminhotemp = self.caminho.upper()
        caminhoarquivo = destino + '\\' + os.path.basename(caminhotemp.replace('.TXT', '_tratado.TXT'))

        with open(caminhoarquivo, 'w', encoding='ANSI') as arquivo:
            for linhalista in self.listaarquivo:
                linhalista = [str(campo).strip() + self.separador for campo in linhalista]
                linhalista = left(linhalista, len(linhalista) - 1)
                arquivo.write(linhalista + '\n')
                linhalista = ''

        return caminhoarquivo

    def retornalistadedicionario(self):
        """
        :return: transforma a lista resultante do arquivo em dicionário com os cabeçalhos.
        """
        cabecalhoacertado = [campo.strip() for campo in self.cabecalho]
        listofdict = [dict(zip(cabecalhoacertado, line)) for line in self.listaarquivo]
        return listofdict

    def retornadf(self, campovalor='', adicionafornecedor=False):
        """
        :param campovalor: nome do campo a ser tratado como valor (põe em float também)
        :return:
        """
        listafornecedores = []
        # Tira os espaços dos nomes dos cabeçalhos
        inicioetapa = time.time()
        mensagemetapa = 'Acertando Cabeçalho...'
        print(mensagemetapa)

        cabecalhoacertado = [campo.strip() for campo in self.cabecalho]
        # Cria um "data frame" com os dados do arquivo na lista de listas de nome "ListaArquivo" e coloca cada um com o
        # respetivo cabeçalho que está na lista de cabeçalhos
        fimetapa = time.time()
        inicioetapa = tratatempo(inicioetapa, fimetapa, mensagemetapa)
        mensagemetapa = 'Criando Dataframe...'
        print(mensagemetapa)

        df = pd.DataFrame(self.listaarquivo, columns=cabecalhoacertado)
        fimetapa = time.time()
        inicioetapa = tratatempo(inicioetapa, fimetapa, mensagemetapa)
        mensagemetapa = 'Tirando colunas vazias...'
        print(mensagemetapa)

        # Inicia a variável de "Sem Valor" do Python
        nan_value = float("NaN")
        # Substitui a variável vazia por sem valor
        df.replace('', nan_value, inplace=True)
        # Apaga a coluna que só tem informações sem valor
        df.dropna(how='all', axis=1, inplace=True)
        # Devolve o vazio padrão para as células vazias
        df.replace(nan_value, '', inplace=True)

        fimetapa = time.time()
        inicioetapa = tratatempo(inicioetapa, fimetapa, mensagemetapa)
        mensagemetapa = 'Acertando os valores...'
        print(mensagemetapa)

        if len(campovalor) > 0:
            df[campovalor] = df[campovalor].apply(acertavalor)

        if adicionafornecedor:
            fimetapa = time.time()
            inicioetapa = tratatempo(inicioetapa, fimetapa, mensagemetapa)
            mensagemetapa = 'Adicionando coluna Fornecedor...'
            print(mensagemetapa)

            totalinhas = len(df.index)
            with tqdm(total=totalinhas) as barra_progresso:
                for indice, linha in enumerate(df['Tipo']):
                    listafornecedores.append(listarnumeros(list(df['Tipo'].values)[indice], list(df['Texto'].values)[indice], True))
                    barra_progresso.update()

            df['Fornecedores'] = listafornecedores

        fimetapa = time.time()
        inicioetapa = tratatempo(inicioetapa, fimetapa, mensagemetapa)

        # Retorna o dataframe tratado
        return df


def acertavalor(valor):
    """
    :param valor: valor a ser tratado.
    :return:
    """
    if "-" in valor:
        valor = valor.replace('-', '')
        valor = valor.replace('.', '')
        valor = valor.replace(',', '.')
        valor = float(valor)
        valor = valor * -1
    else:
        valor = valor.replace('.', '')
        valor = valor.replace(',', '.')
        valor = float(valor)

    valor = '{:,.2f}'.format(valor)
    return valor


def to_raw(string):
    """
    :param string: string para ser tratado.
    :return:
    """
    return fr"{string}"


def tratatempo(inicioetapa, fimetapa, mensagemetapa):
    tempoetapa = fimetapa-inicioetapa
    hours, rem = divmod(tempoetapa, 3600)
    minutes, seconds = divmod(rem, 60)
    print(mensagemetapa + " " + f'{"{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), int(seconds))}')
    return fimetapa
