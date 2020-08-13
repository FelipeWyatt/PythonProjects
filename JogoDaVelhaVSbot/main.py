import numpy as np
import BOT
from random import choice
import pandas as pd


def mostra(tab):
  tab1 = [[0,0,0],[0,0,0],[0,0,0]]
  for i in range(3):
    for j in range(3):
      if tab[i][j] == 0:
        tab1[i][j] = ' '
      elif tab[i][j] == 1:
        tab1[i][j] = 'X'
      elif tab[i][j] == 2:
        tab1[i][j] = 'O'
  
  print(tab1[0][0]," | ",tab1[0][1]," | ",tab1[0][2])
  print("-------------")
  print(tab1[1][0]," | ",tab1[1][1]," | ",tab1[1][2])
  print("-------------")
  print(tab1[2][0]," | ",tab1[2][1]," | ",tab1[2][2])
  print("\n")



def row_win(board, player):
    lista = np.where(board == player)
    #print(lista)
    
    #print(np.count_nonzero(lista[0] == 0))
    #print(np.count_nonzero(lista[0] == 1))
    #print(np.count_nonzero(lista[0] == 2))
    for i in range(3):
        if np.count_nonzero(lista[0] == i) == 3: #verifica se o primeiro array (linhas) tem 3 zeros, ums ou dois
            return True
    
    return False

def col_win(board, player):
    lista = np.where(board == player)
    for i in range(3):
        if np.count_nonzero(lista[1] == i) == 3: #verifica se o primeiro array (colunas) tem 3 zeros, ums ou dois
            return True
    return False

def diag_win(board, player):
    if board[0,0] == board[1,1] == board[2,2] == player: #verifica se as diagonais estao completas
        return True
    if board[0,2] == board[1,1] == board[2,0] == player:
        return True
    return False

def evaluate(board):
    
    winner = 0
    for player in [1, 2]:
        # add your code here!
        if row_win(board, player) or col_win(board, player) or diag_win(board, player):
            winner = player
    if np.all(board != 0) and winner == 0:
        winner = -1
    return winner

def create_board():
    return np.zeros((3,3), dtype = int)

def place(board, player, position):
    board[position] = player

def user_play(board, player):
    ind = input("Próxima Jogada (linha)(coluna): ")
    i = int(ind[0])
    j = int(ind[1])
    possibilidades = possibilities(board)
    while len(ind) != 2 or i < 0 or i > 2 or j < 0 or j > 2 or ((i,j) not in possibilidades):
        print("Entrada inválida.")
        ind = input("Próxima Jogada (linha)(coluna): ")
        i = int(ind[0])
        j = int(ind[1])
    place(board, player, (i, j))
    
def possibilities(board):
    lista = np.where(board == 0)
    tuplas = []
    for i in range(len(lista[0])):
        tuplas.append((lista[0][i], lista[1][i]))
    return tuplas
    
    
def troca_vez(vez):
    if vez == 1:
        return 2
    elif vez == 2:
        return 1
    else:
        print("Time não existe")
        return 1

    
def user_vs_bot(botStart = True):
    board = create_board()
    vez = 1
    if botStart == False:
        # user joga uma vez antes
        mostra(board)
        user_play(board, vez)
        vez = troca_vez(vez)
    
        
    for i in range(9):
        BOT.bot_play(board, vez)
        vez = troca_vez(vez)
        if evaluate(board) != 0:
            break
        mostra(board)
        
        
        user_play(board, vez)
        #mostra(board)
        vez = troca_vez(vez)
        if evaluate(board) != 0:
            break
    
    mostra(board)
    return evaluate(board)

def bot_vs_random(botStart = True):
    # bot sempre eh 1 e random 2
    bot = 1
    rand = 2
    
    board = create_board()
    if botStart == False:
        # random joga uma vez antes
        place(board, rand, choice(possibilities(board)))
    
        
    for i in range(9):
        BOT.bot_play(board, bot)
        if evaluate(board) != 0:
            break
        
        place(board, rand, choice(possibilities(board)))
        if evaluate(board) != 0:
            break
    
    
    return evaluate(board)

print("[", end = "")
for k in range(2000):
    tabuleiro = np.zeros((3,3), dtype = int)
    for i in range(3):
        for j in range(3):
            tabuleiro[i][j] = choice([0,0,0,1,2])
    if BOT.can_win(tabuleiro, 2) == True: #and evaluate(tabuleiro) == 0:
        #print(tabuleiro)
        print("[", end = "")
        for m in range(3):
            for n in range(3):
                print(tabuleiro[m][n], end = ",")
        print("],")

print("]")
            

"""
# entrada False para o player comecar
winner = user_vs_bot()

if winner == -1:
    print("VELHA")
elif winner == 1:
    print("X WINS")
elif winner == 2:
    print("O WINS")
"""

"""
nJogos = 5000

placar = {'bot':0, 'random':0, 'velha':0}
for i in range(nJogos):
    winner = bot_vs_random()
    if winner == -1:
        placar['velha'] += 1
    elif winner == 1:
        placar['bot'] += 1
    elif winner == 2:
        placar['random'] += 1

tabela = pd.DataFrame(data = placar, index = ["bot começa","random começa" ])

placar = {'velha':0, 'bot':0, 'random':0}
for i in range(nJogos):
    winner = bot_vs_random(0)
    if winner == -1:
        placar['velha'] += 1
    elif winner == 1:
        placar['bot'] += 1
    elif winner == 2:
        placar['random'] += 1

tabela.loc["random começa"] = placar

# porcentagem de vitoria
winRate = []
winRate.append(tabela.loc["bot começa"]['bot']*100/nJogos)
winRate.append(tabela.loc["random começa"]['bot']*100/nJogos)

tabela["bot win %"] = winRate

# Calcula a pontuacao do bot 0-100 (arredondada para baixo).
# vitoria = 1 ponto, velha = 1/2, derrota = 0
pontos = []
num = (tabela.loc["bot começa"]['bot'] + tabela.loc["bot começa"]['velha']*0.5)*100/nJogos
pontos.append(int(num))
num = (tabela.loc["random começa"]['bot'] + tabela.loc["random começa"]['velha']*0.5)*100/nJogos
pontos.append(int(num))

tabela["pontos (0-100)"] = pontos

print(tabela)
print("\nNumero de jogos:", nJogos*2)

"""
