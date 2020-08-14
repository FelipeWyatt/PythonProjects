from random import choice

def checaTeste(lista):
  n = 3
  if len(lista) != n:
    print("Entrada inválida")
    print("A senha só tem %d algarismos" % n)
    return False
  
  algs = []
  for i in range(len(lista)):
    if not lista[i].isdigit():
      print("Entrada inválida")
      print("Digite somente numeros")
      return False
    if lista[i] in algs:
      print("Entrada inválida")
      print("Nao repita algarismos")
      return False
    algs.append(lista[i])
  return True

def recebeTeste():
  teste0 = list(input("Tente uma senha: "))
  while not checaTeste(teste0):
    teste0 = list(input("Tente uma senha: "))
  return teste0

def criptografe(lista, chave, nElementos):
  lista0 = lista.copy()
  num = chave*nElementos
  combinacao = []
  pos = 0
  for numero in chave:
    pos += int(numero)
  for vez in range(nElementos):
    iNum = 0
    incremento = int(num[iNum])
    pos += incremento
    while pos >= len(lista0):
      pos = pos - len(lista0)
    elem = lista0[pos]
    combinacao.append(elem)
    lista0.remove(elem)
    iNum += 1
  
  return combinacao

def avaliaTeste(teste):
  certosLugarErrado = 0
  certosLugarCerto = 0
  for i in range(len(teste)):
    if teste[i] == senha[i]:
      certosLugarCerto += 1
    elif teste[i] in senha:
      certosLugarErrado += 1
  
  print("Algarismos certos em lugar errado: %d" % certosLugarErrado)
  print("Algarismos certos em lugar certo: %d" % certosLugarCerto)

cod = input("Codigo do jogo: ")
nJogad = int(cod[0])
personagensDisponiv = ['Aang', 'Babu', 'Cadu', 'Grey','Habib','Jade', 'Mia', 'Pierre', 'Sher','Tony']
chave1 = cod[2:5]
personagens = criptografe(personagensDisponiv, chave1, nJogad)
personagens.sort()
algarismos = ['0','1','2','3','4','5','6','7','8','9']
chave2 = cod[6:9]
senha = criptografe(algarismos, chave2, 3)
papeis = [False for i in range(nJogad - 1)]
papeis.append(True)
chave3 = cod[10:13]
ehGuarda = criptografe(papeis, chave3, nJogad)
for i in range(len(ehGuarda)):
  if ehGuarda[i]:
    indiceGuarda = i
    break
GUARDA = personagens[indiceGuarda]
print()
print("-"*30)
print("OPEN THE SAFE - Regras")
print("Há dois times: Ladrões e um Guarda. O objetivo dos Ladrões é cooperar para tentar descobrir a senha do cofre.\nO objetivo do Guarda é confundir os Ladrões para impedir o roubo.")
print("A senha é composta de 3 algarismos sem repetição. A cada chute é mostrado quantos algarismos estão certos nos lugares certos e nos lugares errados.")
print("Cada Ladrão pode tentar uma vez uma senha.")
print("O Guarda pode testar uma senha para também ter informações sobre ela.")
print("Podem jogar de 3-9 jogadores")
print("Esse jogo conta com a honestidade, portanto não escolha o mesmo personagem que outro jogador e não reinicie o jogo usando o mesmo código.")
print("-"*30)
print()
print("Escolha um desses personagens, diferente dos outros jogadores")
for player in personagens:
  print(player, end = "   ")
entrada = input("\n")
while entrada not in personagens:
  print("Digite um nome valido")
  entrada = input()
meuJogador = entrada
print()
if meuJogador == GUARDA:
  print("Voce é Guarda.\nEvite que o cofre seja aberto!\n")
else:
  print("Voce é Ladrão.\nTente abrir o cofre com os outros Ladrões.\nVoce só tem uma tentativa!\n")
if nJogad <= 5:
  print("Dica: _{}_".format(senha[1]))
teste = recebeTeste()
if teste == senha:
  if meuJogador == GUARDA:
    print("\nVocê acertou a senha!\n")
    print("Agora você tem grande poder! Impeça aqueles ladrões")
  else:
    print("\nO cofre abre e...\n")
    finais = ["Vocês encontram 700 kg de Ouro!", "Vocês ficam R$5.000.000 mais ricos!", "Cada um agora tem um colar de diamantes!", "Vocês encontram R$10.000.000 em dinheiro!", "Agora cada um pode comprar um time da NBA!", "Vocês estão mais ricos que o Bill Gates"]
    print(choice(finais))
  print()
else:
  avaliaTeste(teste)
input("\nEnter para fechar o jogo: ")
