# Projetos-Oi

Projeto pega os arquivos do SAP e realiza um leitura linha a linha para realizar a 
limpeza de cabeçalhos intermediários e quebras de página que ocorre quando extraímos 
o arquivos em background ou na opção TXT. Nesses casos o SAP "cria" uma "página" no estilo
DOS separada por pipline com colunas de tamanho fixo e com cabeçalhos separados por "-". Outro
tratamento que o mesmo realiza é tratar os "ENTER" (Carriage return) dos campos textos livres
que o usuário possa colocar e acabar "quebrando" a linha antes do seu final. O código toma como 
premissa que o relatório que está sendo tratado não tem os "cabeçalhos de filtro", caso isso ocorra
a variável quantcolunas deve ser definida com o número de colunas do relatório (o padrão é 0) para
que o código possa "ignorar" os cabeçalhos de filtro e achar a primeira linha que tem a quantidade
de colunas informadas na variável, vale lembrar que ele considera as coluna de início e de final como coluna. 
Ex:
|Col1|Col2|Col3|

No exemplo acima a variável teria que ser igual a 5 (cinco) porque ele considera que tem um coluna vazia no início
e no final pois a linha inicia e começa com "|" e quando usa o split para quebrar a linha pelo separador o vetor 
resultante ficará com essas 2 colunas em branco (o código trata isso fazendo com que o arquivo resultante não comece
nem termine com pipline ("|")
