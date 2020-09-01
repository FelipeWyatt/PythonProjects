import json
from classes import Data


# Exemplo da classe de data
#evento = Data("29/5/20", "13h00")
#evento.show()
#print("horas ate o evento:", evento.horasDesdeHoje())



nomeUsuario = 'Felipe'
#coloque a quantidade de horas reservadas por estudo num dia
hEstudo_Dia = 6
"""

tarefas = {
  "08/05/20": {
    "Lista 6 Calculo": {
      "feito": False,
      "tempoExec": 3  # Previsao do tempo em horas
    }
  }
}
"""


#                   string  dict(como do exemplo)
#   '09/05/20'  {'Atividade 6 Materiais':{'feito':False, 'tempoExec':2}}
def adicionarTarefa(data, Tarefa):
  # Transforma o json em um diconario de python
  with open("calendario.json", "r") as write_file:
    dicTarefas = json.load(write_file)
    write_file.close()

  if data in dicTarefas:
    # ja existe essa data catalogada
    nome = list(Tarefa.keys())[0]
    if nome in dicTarefas[data]:
      print("Erro: Essa tarefa já existe")
    else:
      dicTarefas[data][nome] = Tarefa[nome]
      print("Tarefa adicionada com sucesso.")
  else:
    # cria a data no dicionario
    dicTarefas[data] = Tarefa
    # Exemplo
    # dicTarefas['10/05/20'] = {'Tarefa Lab Fisica':{'feito':False, 'tempoExec':2}}

  # Transforma o dicionario de python em json
  with open("calendario.json", "w") as write_file:
    json.dump(dicTarefas, write_file, indent = 2)
    write_file.close()
  
def reescreveCalendario(dicionario):
  # Transforma o dicionario de python em json
  with open("calendario.json", "w") as write_file:
    json.dump(dicionario, write_file, indent = 2)
    write_file.close()

def getCalendario():
  # Transforma o json em um diconario de python
  with open("calendario.json", "r") as write_file:
    dicTarefas = json.load(write_file)
    write_file.close()

  # Transforma o dicionario de python em json
  with open("calendario.json", "w") as write_file:
    json.dump(dicTarefas, write_file, indent = 2)
    write_file.close()
  
  return dicTarefas
  

#                 list
def recebeComando(comandosPossiveis, entrada):
  entrada = entrada.lower()
  try:
    # primeiro procura se o comando foi escrito corretamente
    comandosPossiveis.index(entrada)
    return entrada
  except:
    # procura o comando mais parecido
    for comando in comandosPossiveis:
      if entrada[:2] == comando[:2]:
        return comando
    return -1
  

#adicionarTarefa('11/05/20', {'Lab04':{'feito':False, 'tempoExec':7}})

print("---------------CALENDARIO---------------")
print("Bem Vindo {}.\nQual função deseja: adicionar, concluir, editar, status ou sair.".format(nomeUsuario))
ListaComandos = ['adicionar', 'concluir', 'editar', 'status', 'sair']
comando = recebeComando(ListaComandos, input())
# Caso digitado o comando errado
while comando == -1:
  print("\nErro: Comando não reconhecido")
  print("Qual função deseja: adicionar, concluir, editar, status ou sair.")
  comando = recebeComando(ListaComandos, input())

if comando == 'sair':
  pass

elif comando == 'adicionar':
  print("\nFUNÇÃO ADICIONAR")
  print("Coloque os dados da tarefa.")
  tarefa = {}
  nome = input("Titulo: ")
  data = input("Data de entrega (dd/mm/aa): ")
  tempo = int(input("Estimativa de duração em horas: "))
  tarefa[nome] = {'feito': False, 'tempoExec': tempo}
  adicionarTarefa(data, tarefa)

elif comando == 'concluir':
  print("\nFUNÇÃO CONCLUIR")
  # printa tarefas do calendario
  calendario = getCalendario()
  print("Tarefas pendentes:")
  for data in calendario:
    for tarefa in calendario[data].keys():
      if calendario[data][tarefa]['feito'] == False:
        print("- " + tarefa)

  tarefaConcluida = input("Concluir: ")
  achou = False
  for data in calendario:
    if tarefaConcluida in calendario[data].keys():
      calendario[data][tarefaConcluida]['feito'] = True
      achou = True
  
  if achou:
    reescreveCalendario(calendario)
    print("Tarefa concluida com sucesso.")
  else:
    print("Erro: Tarefa não encontrada")

elif comando == 'editar':
  # criar prog que edita a tarefa
  print("\nFUNÇÃO EDITAR")
  # printa tarefas do calendario
  calendario = getCalendario()
  print("Tarefas Abertas:")
  for data in calendario:
    for tarefa in calendario[data].keys():
      if calendario[data][tarefa]['feito'] == False:
        print("- " + tarefa)


  tarefaEdita = input("Editar a tarefa: ")
  achou = False
  for data in calendario:
    if tarefaEdita in calendario[data].keys():
      aux = {tarefaEdita:{'feito':calendario[data][tarefaEdita]['feito'], 'tempoExec':calendario[data][tarefaEdita]['tempoExec']}}
      
      #print("Aux: ", aux)
      # Apaga a tarefa e escreve denovo
      del calendario[data][tarefaEdita]

      novoNome = input("{} -> ".format(tarefaEdita))
      novaData = input("{} -> ".format(data))

      novo = {novoNome:{}}

      novo[novoNome]['feito'] = bool(input("{} -> ".format(aux[tarefaEdita]['feito'])))
      novo[novoNome]['tempoExec'] = int(input("{} -> ".format(aux[tarefaEdita]['tempoExec'])))

      adicionarTarefa(novaData, novo)

      achou = True
  
  if achou:
    print("Tarefa editada com sucesso.")
  else:
    print("Erro: Tarefa não encontrada")


elif comando == 'status':
  # criar prog que mostra as tarefas que devem ser feitas hoje e o calendario em si 

  print("\nSTATUS")
  # printa tarefas do calendario
  calendario = getCalendario()
  print("\nTarefas Concluídas:")
  for data in calendario:
    for tarefa in calendario[data].keys():
      if calendario[data][tarefa]['feito'] == True:
        print("- " + tarefa)

  ordem = {}
  print("\nTarefas pendentes:")
  for data in calendario:
    for tarefa in calendario[data].keys():
      if calendario[data][tarefa]['feito'] == False:
        print("- {} ({})".format(tarefa, data))

        # calcula o tempo restante ate a entrega da lista no dia data 23h59
        d = Data(data)
        # transforma horas em dias
        ordem[tarefa] = (round(d.horasDesdeHoje()/24))*hEstudo_Dia
        ordem[tarefa] -= calendario[data][tarefa]['tempoExec']
  
  print("\nAconselho realizar as tarefas na seguinte ordem:")
  menor = list(ordem.keys())[0]
  while True:
    # encontra a chave do menor valor
    for chave in ordem:
      if ordem[chave] < ordem[menor]:
        menor = chave
    print(menor, "(fator = {})".format(ordem[menor]))
    del ordem[menor]
    if len(list(ordem.keys())) == 0:
      break
    menor = list(ordem.keys())[0]

  
  for key in ordem:
    print(key, ":",ordem[key])
  
