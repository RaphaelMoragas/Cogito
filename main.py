# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pygame
import random

# Inicialização do Pygame
pygame.init()

# Configurações da tela
tam_grade = 9
tam_cel = 60
tam_tela = tam_cel * tam_grade
tela = pygame.display.set_mode((tam_tela, tam_tela))
pygame.display.set_caption('Jogo Cogito')

# Cores
cor_fundo = (30, 30, 30)
cor_grade = (60, 60, 60)
cor_peca = (200, 200, 50)

# Tabuleiro
tab = [[0] * tam_grade for _ in range(tam_grade)]

def colocar_pecas():
    for _ in range(9):
        while True:
            x, y = random.randint(0, tam_grade - 1), random.randint(0, tam_grade - 1)
            if tab[y][x] == 0:
                tab[y][x] = 1
                break

def desenhar():
    tela.fill(cor_fundo)
    for y in range(tam_grade):
        for x in range(tam_grade):
            rect = pygame.Rect(x * tam_cel, y * tam_cel, tam_cel, tam_cel)
            pygame.draw.rect(tela, cor_grade, rect, 1)
            if tab[y][x] == 1:
                pygame.draw.rect(tela, cor_peca, rect)

# inicio chat
def ciclo_lista(lista):
    return lista[-1:] + lista[:-1]

def mover_linha(indice, direcao):
    if direcao == 'esq':
        tab[indice] = ciclo_lista(tab[indice])
    elif direcao == 'dir':
        tab[indice] = list(reversed(ciclo_lista(list(reversed(tab[indice])))))

def mover_coluna(indice, direcao):
    coluna = [tab[i][indice] for i in range(tam_grade)]
    if direcao == 'cim':
        coluna = ciclo_lista(coluna)
    elif direcao == 'bai':
        coluna = list(reversed(ciclo_lista(list(reversed(coluna)))))
    for i in range(tam_grade):
        tab[i][indice] = coluna[i]

def processa_clique(x, y):
    if x < tam_cel:  # Botão esquerdo para linhas
        indice = y // tam_cel
        mover_linha(indice, 'esq')
    elif x > tam_tela - tam_cel:  # Botão direito para linhas
        indice = y // tam_cel
        mover_linha(indice, 'dir')
    elif y < tam_cel:  # Botão superior para colunas
        indice = x // tam_cel
        mover_coluna(indice, 'cim')
    elif y > tam_tela - tam_cel:  # Botão inferior para colunas
        indice = x // tam_cel
        mover_coluna(indice, 'bai')

        #fim chat

def jogo():
    colocar_pecas()
    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                processa_clique(x, y)

        desenhar()
        pygame.display.flip()

    pygame.quit()

# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    jogo()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
