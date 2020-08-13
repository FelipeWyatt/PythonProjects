from random import choice
import numpy as np


def possibilities(board):
    lista = np.where(board == 0)
    tuplas = []
    for i in range(len(lista[0])):
        tuplas.append((lista[0][i], lista[1][i]))
    return tuplas



def row_win(board, player):
    lista = np.where(board == player)
    
    for i in range(3):
        if np.count_nonzero(lista[0] == i) == 3: #verifica se o primeiro array (linhas) tem 3 zeros, ums ou dois
            return True
    
    return False

def col_win(board, player):
    lista = np.where(board == player)
    for i in range(3):
        if np.count_nonzero(lista[1] == i) == 3: #verifica se o segundo array (colunas) tem 3 zeros, ums ou dois
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

def can_win(board, player):
    """ verifica se falta um espaço para algum dos jogadores, retorna tupla
    (b,c). Onde (b,c) as coordenadas do lugar que ganha o jogo, se o player não
    pode ganhar então b = c = -1
    """
    
    # verifica as linhas
    ind = -1
    for linha in range(3):
        l = board[linha,:] # vetor com tamanho 3
        if  sorted(l) == [0, player, player] :
            # Verifica se da pra ganhar o jogo
            # salva o indice do zero
            ind = np.where(l == 0)[0][0] # np.where retorna uma tupla de arrays, cada array indica o indice na dimensao
            break
    if ind != -1:
        return (linha, ind)
    
    # verifica as colunas
    for coluna in range(3):
        l = board[:, coluna] # vetor com tamanho 3
        if  sorted(l) == [0, player, player] :
            # Verifica se da pra ganhar o jogo
            # salva o indice do zero
            ind = np.where(l == 0)[0][0] # np.where retorna uma tupla de arrays, cada array indica o indice na dimensao
            break
    if ind != -1:
        return (ind, coluna)
    
    
    # verifica a diagonal principal
    l = board.diagonal() # vetor com tamanho 3
    if  sorted(l) == [0, player, player] :
        # Verifica se da pra ganhar o jogo
        # salva o indice do zero
        ind = np.where(l == 0)[0][0] # np.where retorna uma tupla de arrays, cada array indica o indice na dimensao

    if ind != -1:
        return (ind, ind)
    
    # verifica a diagonal secundaria
    l = np.fliplr(board).diagonal()  # Horizontal flip # vetor com tamanho 3
    if  sorted(l) == [0, player, player] :
        # Verifica se da pra ganhar o jogo
        # salva o indice do zero
        ind = np.where(l == 0)[0][0] # np.where retorna uma tupla de arrays, cada array indica o indice na dimensao

    if ind != -1:
        return (ind, 2 - ind)
   
    
    return (-1, -1) #caso nao de para ganhar de nenhum modo
    
    

def bot_play(board, player):
    # estrategia 1 é jogar aleatoriamente
    # estrategia 2 é verificar se da pra ganhar, se nao verifica se o user pode ganhar, se nao joga aleatoriamente
    if player == 1:
        oponente = 2
    elif player == 2:
        oponente = 1
    
    teste = can_win(board, player)
    if teste != (-1,-1):
        # pra ganha o jogo
        board[teste] = player
        return board
    
    teste = can_win(board, oponente)
    if teste != (-1,-1):
        # pra evitar que o user ganhe o jogo
        board[teste] = player
        return board
    
    if board[1][1] == 0:
        # joga no meio se possivel
        board[1,1] = player
        return board
        
    # joga aleatoriamente
    selections = possibilities(board)
    if len(selections) > 0:
        selection = choice(selections)
        board[selection] = player
    return board 

