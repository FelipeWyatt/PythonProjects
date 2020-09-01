from datetime import datetime, timedelta
from tabulate import tabulate
import json

#---------------------CLASSES----------------------

# Exemplo da classe de data
# evento = Data("29/5/20", "13h00")
# evento.show()
# print("horas ate o evento:", evento.horasDesdeHoje())

class Data:
  #                 "DD/MM/AA"           "HHhMM"
  def __init__(self, dataString, horas = "23h59"):
    lista = []
    for num in dataString.split("/"):
      if not num.isdigit():
        return print("Sintaxe errada da data!")
      else:
        lista.append(int(num))
    
    for num in horas.split("h"):
      if not num.isdigit():
        return print("Sintaxe errada da hora!")
      else:
        lista.append(int(num))

    
    if lista[0] <= 0 or lista[0] > 31:
      return print("Dia invalido para data!")
    if lista[1] <= 0 or lista[1] > 12:
      return print("Mes invalido para data!")
    if lista[2] <= 0 or lista[2] > 9999:
      return print("Ano invalido para data!")
    if lista[3] < 0 or lista[3] > 23:
      return print("Hora invalida para data!")
    if lista[4] < 0 or lista[4] > 59:
      return print("Minuto invalido para data!")
    
    self.dia = lista[0]
    self.mes = lista[1]
    self.ano = lista[2]
    self.hora = lista[3]
    self.minuto = lista[4]

  def get(self, printa):
    # se printa eh True, entao vai printar a string do tempo
    # printa inteiro com 2 algarismos
    string = "{:02d}/{:02d}/{:02d} {:02d}h{:02d}".format(self.dia, self.mes, self.ano, self.hora, self.minuto)
    if printa:
      print(string)
    return string
  
  

  def horasDesdeHoje(self):
    # retorna os horas de hoje ate a Data
    diferenca = datetime(2000+self.ano, self.mes, self.dia, self.hora, self.minuto) - ( datetime.now() - timedelta(hours = 3))
    # arruma fuso horario q eh 3 horas avancado

    #print("hoje:", datetime.now() - timedelta(hours = 3))
  
    return round(diferenca.total_seconds()/(3600))
  

#---------------------FUNCOES----------------------
# FUNCOES DO CALENDARIO

def getCalendario():
  # abre json e retorna um dicionario em python
  with open("calendario.json", "r") as write_file:
    dicTarefas = json.load(write_file)
    write_file.close()

  return dicTarefas

def rewriteCalendario(dicionario):
  # Transforma o dicionario de python em json
  with open("calendario.json", "w") as write_file:
    json.dump(dicionario, write_file, indent = 2)
    write_file.close()


def adicionarTarefa(data, Tarefa):
  # Adiciona a tarefa a uma data
  # Exemplo:  '09/05/20 23h59'  {'Atividade 6 Materiais':{'feito':False, 'tempoExec':2}}
  
  dicTarefas = getCalendario()

  if data in dicTarefas:
    # ja existe essa data catalogada
    nome = list(Tarefa.keys())[0] # titulo da atividade

    if procuraTarefa(nome):
      print("Erro: Essa tarefa já existe")
    else:
      dicTarefas[data][nome] = Tarefa[nome]
      print("Sucesso.")
  else:
    # cria a data no dicionario
    dicTarefas[data] = Tarefa

  rewriteCalendario(dicTarefas)

def procuraTarefa(titulo):
  # Procura o titulo de uma tarefa no calendario ou titulos parecidos (ignora espacos e "de"/"do")
  # Exemplo:  'Atividade 6 Materiais'
  
  dicTarefas = getCalendario()

  for data in dicTarefas:
    for nome in dicTarefas[data]:
      a = set(nome.lower().split())
      b = set(titulo.lower().split())
      #tenta remover os intes da lista
      for remover in ['de', 'do', 'da', '-']:
        try:
          a.remove(remover)
        except:
          pass
        try:
          b.remove(remover)
        except:
          pass
      
      # compara os titulos sem palavras intermediarias
      if a == b:
        return True
  
  return False


# FUNCOES AUXILIARES

def recebeEntradaTipo(msgInput, entradaEsperada, minimo = "", maximo = ""):
  # exemplos de entradaEsperada
  # "**/**/**" -> * eh um digito, barra eh caractere
  # "**h**" -> * eh um digito, h eh caractere
  # exemplos minimo e maximo:
  # "00h00", "23h59"

  if minimo == maximo == "": # realiza a func normalmente
    variavel = input(msgInput)

    # caso especial de hora default
    if entradaEsperada == "**h**" and variavel == "":
      return "23h59"

    # verifica se data esta na forma certa
    condicao = True
    if len(variavel) != len(entradaEsperada):
        condicao = False
    else: # ambos tem o mesmo tamanho
      # verifica se eh numero onde deve ser e se o resto dos caracteres sao iguais
      for i in range(len(variavel)):
        if entradaEsperada[i] == "*":
          if not variavel[i].isdigit():
            condicao = False
            break
        else:
          if entradaEsperada[i] != variavel[i]:
            condicao = False
            break
  
    # se n passou nas condicoes vai pedir para redigitar a entrada ate digitar corretamente
    while condicao == False:
      print("Erro na entrada, redigite.")
      variavel = input(msgInput)

      condicao = True
      if len(variavel) != len(entradaEsperada):
        condicao = False
      else: # ambos tem o mesmo tamanho
        # verifica se eh numero onde deve ser e se o resto dos caracteres sao iguais
        for i in range(len(variavel)):
          if entradaEsperada[i] == "*":
            if not variavel[i].isdigit():
              condicao = False
              break
          else:
            if entradaEsperada[i] != variavel[i]:
              condicao = False
              break
  
  else: # tem condicoes a mais -> minimos e maximos
    variavel = input(msgInput)

    # caso especial de hora default
    if entradaEsperada == "**h**" and variavel == "":
      return "23h59"

    # verifica se data esta na forma certa
    condicao = True
    if len(variavel) != len(entradaEsperada):
        condicao = False
    else: # ambos tem o mesmo tamanho
      # verifica se eh numero onde deve ser e se o resto dos caracteres sao iguais
      for i in range(len(variavel)):
        if entradaEsperada[i] == "*":
          if not variavel[i].isdigit():
            condicao = False
            break
        else:
          if entradaEsperada[i] != variavel[i]:
            condicao = False
            break
      
      # transforma cada entrada da funcao em lista de numeros sem os separadores
      listaMin = []
      num = ""
      for carac in minimo:
        if carac.isdigit():
          num += carac
        elif len(num) > 0:
          listaMin.append(int(num)) 
          num = ""
      if len(num) > 0:
        listaMin.append(int(num))

      listaMax = []
      num = ""
      for carac in maximo:
        if carac.isdigit():
          num += carac
        elif len(num) > 0:
          listaMax.append(int(num)) 
          num = ""
      if len(num) > 0:
        listaMax.append(int(num))

      listaEntrada = []
      num = ""
      for carac in variavel:
        if carac.isdigit():
          num += carac
        elif len(num) > 0:
          listaEntrada.append(int(num)) 
          num = ""
      if len(num) > 0:
        listaEntrada.append(int(num))
    
      # verifica se a entrada esta dentro dos max e min
      for i in range(len(listaEntrada)):
        if not (listaMin[i] <= listaEntrada[i] <=  listaMax[i]):
          condicao = False
          break

  
    # se n passou nas condicoes vai pedir para redigitar a entrada ate digitar corretamente
    while condicao == False:
      print("Erro na entrada, redigite.")
      variavel = input(msgInput)

      condicao = True
      if len(variavel) != len(entradaEsperada):
          condicao = False
      else: # ambos tem o mesmo tamanho
        # verifica se eh numero onde deve ser e se o resto dos caracteres sao iguais
        for i in range(len(variavel)):
          if entradaEsperada[i] == "*":
            if not variavel[i].isdigit():
              condicao = False
              break
          else:
            if entradaEsperada[i] != variavel[i]:
              condicao = False
              break
        
        # transforma cada entrada da funcao em lista de numeros sem os separadores
        listaMin = []
        num = ""
        for carac in minimo:
          if carac.isdigit():
            num += carac
          elif len(num) > 0:
            listaMin.append(int(num)) 
            num = ""
        if len(num) > 0:
          listaMin.append(int(num))

        listaMax = []
        num = ""
        for carac in maximo:
          if carac.isdigit():
            num += carac
          elif len(num) > 0:
            listaMax.append(int(num)) 
            num = ""
        if len(num) > 0:
          listaMax.append(int(num))

        listaEntrada = []
        num = ""
        for carac in variavel:
          if carac.isdigit():
            num += carac
          elif len(num) > 0:
            listaEntrada.append(int(num)) 
            num = ""
        if len(num) > 0:
          listaEntrada.append(int(num))

        # verifica se a entrada esta dentro dos max e min
        for i in range(len(listaEntrada)):
          if not (listaMin[i] <= listaEntrada[i] <=  listaMax[i]):
            condicao = False
            break


  return variavel


def recebeComando(comandosPossiveis, entrada):
  # Reconhe o comando entrado e retorna indice do comando na lista de comandos
  # Caso nao encontre retorna -1
  # Exemplo:    lista de strings    string do input
  entrada = entrada.lower()
  try:
    # primeiro procura se o comando foi escrito corretamente
    comandosPossiveis.index(entrada)
    return entrada
  except:
    # procura o comando mais parecido
    for comando in comandosPossiveis:
      if entrada[:2] == comando[:2]:  # analisa as duas primeiras letras
        return comando
    return -1


# FUNCOES DE COMANDO


def main(nomeUsuario, hEstudo_Dia):
  ListaComandos = ['adicionar', 'concluir', 'editar', 'status', 'sair']

  print("---------------CALENDARIO---------------")
  print("Bem Vindo {}.\nQual função deseja: adicionar, concluir, editar, status ou sair.".format(nomeUsuario))
  comando = recebeComando(ListaComandos, input())
  # Caso digitado o comando errado
  while comando == -1:
    print("\nErro: Comando não reconhecido")
    print("Qual função deseja: adicionar, concluir, editar, status ou sair.")
    comando = recebeComando(ListaComandos, input())
  
  if comando == 'adicionar':
    adicionar()
  elif comando == 'concluir':
    concluir()
  elif comando == 'editar':
    editar()
  elif comando == 'status':
    status(hEstudo_Dia)
  elif comando == 'sair':
    return
  
  
  while True:
    print("\nQual função deseja: adicionar, concluir, editar, status ou sair.".format(nomeUsuario))
    comando = recebeComando(ListaComandos, input())
    # Caso digitado o comando errado
    while comando == -1:
      print("\nErro: Comando não reconhecido")
      print("Qual função deseja: adicionar, concluir, editar, status ou sair.")
      comando = recebeComando(ListaComandos, input())

    if comando == 'adicionar':
      adicionar()
    elif comando == 'concluir':
      concluir()
    elif comando == 'editar':
      editar()
    elif comando == 'status':
      status(hEstudo_Dia)
    elif comando == 'sair':
      return

def adicionar():
  print("FUNÇÃO ADICIONAR")
  print("Coloque o Nome da nova tarefa.")
  tarefa = {}
  nome = input("Título: ")
  if procuraTarefa(nome):
    print("Essa tarefa já existe.")
    return
  
  data = recebeEntradaTipo("Data de entrega (dd/mm/aa): ", "**/**/**", "01/01/00", "31/12/99")

  horario = recebeEntradaTipo("Horário de entrega (default = 23h59): ", "**h**", "00h00", "23h59")

  tempo = int(input("Estimativa de duração em horas: "))
  condicao = tempo > 0
  # checa se tempo é positivo != 0
  while condicao == False:
    print("Estimativa de tempo inválida, redigite.")
    tempo = int(input("Estimativa de duração em horas: "))
    condicao = tempo > 0

  tarefa[nome] = {'feito': False, 'tempoExec': tempo}

  adicionarTarefa(data + " " + horario, tarefa)

def concluir():
  print("\nFUNÇÃO CONCLUIR")
  # printa tarefas do calendario
  calendario = getCalendario()

  print("Tarefas pendentes:")
  pendentes = []
  for data in calendario:
    for tarefa in calendario[data].keys():
      if calendario[data][tarefa]['feito'] == False:
        # coloca as tarefas pendentes numa lista para associar a cada numero
        pendentes.append(tarefa)
  
  for i in range(len(pendentes)):
    print("{}) {}".format(i+1, pendentes[i]))
    

  tarefaConcluida = input("Concluir: ")

  if tarefaConcluida.isdigit():
    # digitou pela numeracao, achar o nome da tarefa a ser concluida
    tarefaConcluida = pendentes[int(tarefaConcluida) - 1]

  achou = False
  for data in calendario:
    if tarefaConcluida in calendario[data].keys():
      calendario[data][tarefaConcluida]['feito'] = True
      achou = True
  

  if achou:
    rewriteCalendario(calendario)
    print("Tarefa concluida com sucesso.")
  else:
    print("Erro: Tarefa não encontrada")


def editar():
  # criar prog que edita a tarefa
  print("\nFUNÇÃO EDITAR")
  # printa tarefas do calendario
  calendario = getCalendario()
  
  print("Tarefas abertas:")
  abertas = []
  for data in calendario:
    for tarefa in calendario[data].keys():
      # coloca as tarefas do calendario numa lista para associar a cada numero
      abertas.append(tarefa)
  
  for i in range(len(abertas)):
    print("{}) {}".format(i+1, abertas[i]))
    

  tarefaEditar = input("Editar a tarefa: ")

  if tarefaEditar.isdigit():
    # digitou pela numeracao, achar o nome da tarefa a ser concluida
    tarefaEditar = abertas[int(tarefaEditar) - 1]

  achou = False
  for data in calendario:
    if tarefaEditar in calendario[data].keys():
      aux = {tarefaEditar:{'feito':calendario[data][tarefaEditar]['feito'], 'tempoExec':calendario[data][tarefaEditar]['tempoExec']}}
      
      #print("Aux: ", aux)
      # Apaga a tarefa antiga
      
      del calendario[data][tarefaEditar]
      rewriteCalendario(calendario)

      novoNome = input("Nome: {} -> ".format(tarefaEditar))
      if novoNome == "":
        print(tarefaEditar)
        novoNome = tarefaEditar 
      novaData = input("Data: {} -> ".format(data))
      if novaData == "":
        print(data)
        novaData = data 
      novo = {novoNome:{}}

      novoFeito = input("Feito: {} -> ".format(aux[tarefaEditar]['feito']))
      if novoFeito.lower() == "true":
        novoFeito = True
      else:
        print(False)
        novoFeito = False

      novo[novoNome]['feito'] = novoFeito

      X = input("Tempo Exec.: {} -> ".format(aux[tarefaEditar]['tempoExec']))
      if X == "":
        X = aux[tarefaEditar]['tempoExec']
        print(X)
      novo[novoNome]['tempoExec'] = int(X)
      

      adicionarTarefa(novaData, novo)

      achou = True
  
  if achou:
    print("Tarefa editada.")
  else:
    print("Erro: Tarefa não encontrada")



def status(hEstudo_Dia):
  # criar prog que mostra as tarefas que devem ser feitas hoje e o calendario em si 

  print("\nSTATUS")
  # printa tarefas do calendario
  calendario = getCalendario()
  print("\nTarefas Concluídas:")
  for data in calendario:
    for tarefa in calendario[data].keys():
      if calendario[data][tarefa]['feito'] == True:
        print("- " + tarefa)
  print()
  
  # printa tarefas na ordem ate a entrega
  ordem = {}
  #print("\nTarefas pendentes:")
  for data in calendario:
    for tarefa in calendario[data].keys():
      if calendario[data][tarefa]['feito'] == False:
        objData = Data(data[:8], data[9:])
        tempoAte = objData.horasDesdeHoje()
        if tempoAte in ordem:
          ordem[tempoAte].add(data)
        else:
          ordem[tempoAte] = set([data])
  
  listaDatas = sorted(ordem)

  P = []
  for i in range(len(listaDatas)):
    for data in ordem[listaDatas[i]]: #sera uma lista com as tarefas para aquela data e horario
      for tarefa in calendario[data]:
        if calendario[data][tarefa]['feito'] == False:
          P.append([tarefa, data])
          #print("{}) {} - {}".format(cont, tarefa, data))
  
  # printa igual tabela
  print(tabulate(P, headers = ["Tarefas pendentes", "Data"], tablefmt = "presto"))
  

  # Gera a ordem indicada para a realizacao das tarefas
  ordem = {}
  for data in calendario:
    for tarefa in calendario[data].keys():
      if calendario[data][tarefa]['feito'] == False:
        # calcula o tempo restante ate a entrega da lista no dia data 23h59
        d = Data(data[:8], data[9:])
        # transforma horas em dias
        ordem[tarefa] = (round(d.horasDesdeHoje()/24))*hEstudo_Dia
        ordem[tarefa] -= calendario[data][tarefa]['tempoExec']
  
  print("\nAconselho realizar as tarefas na seguinte ordem:")
  P = []
  menor = list(ordem.keys())[0]
  while True:
    # encontra a chave do menor valor
    for chave in ordem:
      if ordem[chave] < ordem[menor]:
        menor = chave
    for data in calendario:
      for nome in calendario[data]:
        if nome == menor:
          P.append([menor, calendario[data][menor]['tempoExec']])
          #print("- {} \t {}".format(menor, calendario[data][menor]['tempoExec']))
    del ordem[menor]
    if len(list(ordem.keys())) == 0:
      break
    menor = list(ordem.keys())[0]
  
  print(tabulate(P, headers = ["Tarefa", "TempoExec"], tablefmt = "presto", numalign = "center"))