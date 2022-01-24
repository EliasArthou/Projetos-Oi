import os.path
# import pandas as pd
import re

import pypyodbc

import sensiveis as pwd

def caminhospadroes(caminho):
    # Pegar a pasta "Meus Documentos" do usuário
    import ctypes.wintypes
    csidl_personal = caminho  # Caminho padrão
    shgfp_type_current = 0  # Para não pegar a pasta padrão e sim a definida como documentos

    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.Shell32.SHGetFolderPathW(None, csidl_personal, None, shgfp_type_current, buf)

    return buf.value


def caminhoselecionado(tipojanela=1):
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
        name = filedialog.askdirectory(initialdir=caminhospadroes(5), title='Selecione a Pasta')
        if name is None:  # askdirectory return `None` if dialog closed with "cancel".
            return ''
        text2save = name
        retorno = text2save

    else:
        return

    return retorno


def retornaarquivos(caminho):
    import os

    lista = []

    if len(caminho) > 0:
        for diretorio, subpastas, arquivos in os.walk(caminho):
            for arquivo in arquivos:
                arquivoatual = os.path.join(os.path.realpath(diretorio), arquivo)
                if right(arquivoatual.upper(), 4) == '.TXT':   #Equivalente a 4 dígitos a direita
                    lista.append(os.path.join(os.path.realpath(diretorio), arquivo))
    else:
        return

    return lista


def left(s, amount):
    return s[:amount]


def right(s, amount):
    return s[-amount:]


def mid(s, offset, amount):
    return s[(offset-1):(offset-1)+amount]


def index_of(val, in_list):
    try:
        return in_list.index(val)
    except ValueError:
        return -1
# if tipo.strip() == 'WE' or tipo.strip() == 'AB' or tipo.strip() == 'D6' or tipo.strip() == 'RE':
# elif tipo.strip() == 'EP' or tipo.strip() == 'PV':

def listarnumeros(tipo, texto):

    match tipo:
        case 'WE'|'AB'|'D6'|'RE':
            return re.findall(r'Forn[\D*]*([\d]+)[\D]', texto)

        case 'EP'|'PV':
            return re.findall(r'_([\d]{6,7})_', texto)

        case _:
            return re.findall(r'([\d]{6}[\d]*)[\D]', texto)


class TrabalhaArquivo:
    def __init__(self, caminho):
        self.caminho = caminho
        self.precabecalho = []
        self.listaarquivo = []
        self.cabecalho = ''
        self.quantcampos = 0
        self.separador = ''

    def verificacabecalho(self, separador, quantcampos=0):
        if len(self.separador) == 0:
            self.separador = separador

        with open(self.caminho, 'r', encoding='ANSI') as arquivo:
            texto = arquivo.readlines()
            for linha in texto:
                linha = linha.strip()
                if (left(linha, 1) == separador and right(linha, 1) == separador and quantcampos == 0) or \
                        len(linha.split(separador)) == quantcampos:
                    self.quantcampos = len(linha.split(separador))
                    self.cabecalho = linha
                    break

                else:
                    self.precabecalho.append(linha)

    def acertarlinhaquebrada(self, separador=''):
        linhaanterior = ''
        listalinhascortadas = []
        listalinhasacertadas = []

        if len(self.separador) > 0:
            separadorlocal = self.separador
        else:
            separadorlocal = separador
        if self.quantcampos > 0:
            self.listaarquivo.append(self.cabecalho.split(separadorlocal))
            with open(self.caminho, 'r', encoding='ANSI') as arquivo:
                texto = arquivo.readlines()
                for linha in texto:
                    linha = linha.strip()
                    if index_of(linha, self.precabecalho) != -1 or linha != self.cabecalho:
                        if linha != '-' * len(linha) and mid(linha.replace(' ', ''), 2, 1) != '*':
                            if len(linha.split(separadorlocal)) < self.quantcampos:
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
                                    self.listaarquivo.append(novalinha.split(separadorlocal))
                                    novalinha = ''
                                    linhaanterior = ''
                            else:
                                if len(linha.split(separadorlocal)) == self.quantcampos:
                                    novalinha = ''
                                    linhaanterior = ''
                                    self.listaarquivo.append(linha.split(separadorlocal))
                                else:
                                    camposamais = len(linha.split(separadorlocal))-self.quantcampos
                                    linhainvertida = linha[::-1]
                                    linhainvertida = mid(linhainvertida, 2, len(linhainvertida)-1)

                                    for campos in range(camposamais):
                                        linhainvertida = linhainvertida.replace(separadorlocal, '\t', 1)

                                    linhainvertida = '|'+linhainvertida
                                    linha = linhainvertida[::-1]
                                    self.listaarquivo.append(linha.split(separadorlocal))

                return listalinhascortadas, listalinhasacertadas

    def salvar_arquivo(self, destino, tratarfornecedor=True):
        linhatemp = ''
        caminhotemp = self.caminho.upper()
        caminhoarquivo = destino+'\\'+os.path.basename(caminhotemp.replace('.TXT', '_tratado.TXT'))

        caminhofornecedor = destino+'\\'+os.path.basename(caminhotemp.replace('.TXT', '_fornecedor.TXT'))
        with open(caminhoarquivo, 'w', encoding='ANSI') as arquivo, \
                open(caminhofornecedor, 'w', encoding='ANSI') as arquivoforn:
            for item in self.listaarquivo:
                for campo in item:
                    if len(str(campo)) > 0:
                        linhatemp = linhatemp + str(campo).strip()+self.separador
                linhatemp = left(linhatemp, len(linhatemp)-1)
                if tratarfornecedor:
                    if linhatemp != self.cabecalho:
                        linhaforntemp = linhatemp.split(self.separador)
                        if len(linhaforntemp) > 0:
                            indicelinha = linhaforntemp[0]
                            tipo = linhaforntemp[7]
                            anomes = linhaforntemp[3]
                            texto = linhaforntemp[len(linhaforntemp)-1]
                            #Campo '7' é o campo do Tipo
                            listaforn = listarnumeros(linhaforntemp[7].split(), texto)
                            if len(listaforn) > 0:
                                for campo in listaforn:
                                    if len(str(campo).strip()) > 0:
                                        linhaforn = indicelinha+self.separador+tipo+self.separador+anomes+self.separador+texto+self.separador+str(int(campo)).strip()
                                        if len(linhaforn) > 0:
                                            arquivoforn.write(linhaforn + '\n')
                                        linhaforn = ''
                    else:
                        linhaforn = 'Indice'+self.separador+'Tipo'+self.separador+'AnoMes'+self.separador+'Texto'+self.separador+'Fornecedor'
                        arquivoforn.write(linhaforn + '\n')
                        linhaforn = ''

                arquivo.write(linhatemp+'\n')
                linhatemp = ''

        if not(tratarfornecedor):
            if os.path.isfile(caminhofornecedor):
                os.remove(caminhofornecedor)
            caminhofornecedor=''

        return caminhoarquivo, caminhofornecedor


def acertavalor(valor):
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
    return valor


def to_raw(string):
    return fr"{string}"




#def arquivopandas(caminho):
#    if os.path.isfile(caminho):
#        data = pd.read_csv(caminho, delimiter='|', encoding='ANSI', low_memory=False)
#        data["Mont.em MI"].apply(acertavalor)
#        return data
