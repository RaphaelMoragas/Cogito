# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pygame
import random

# Inicialização do Pygame
pygame.init()
pygame.mixer.init()

# Configurações da tela
tam_grade = 9
tam_cel = 60
larg_borda = tam_cel // 3
tam_tela = tam_cel * tam_grade + larg_borda * 2
tela = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Jogo Cogito')

# Cores
cor_grade = (255, 255, 255)
cor_btn = (0, 255, 255)

# Tabuleiro
tab = [[0] * tam_grade for _ in range(tam_grade)]

# Imagem de fundo
imagem_fundo = pygame.image.load('Files/background.jpg')
imagem_fundo = pygame.transform.scale(imagem_fundo, (1280, 720))

# Imagens
cor_peca = pygame.image.load('Files/orb.jpeg')
imagem_peca = pygame.transform.scale(cor_peca, (tam_cel, tam_cel))
imagem_peca_ref = pygame.transform.scale(cor_peca, (tam_cel // 3, tam_cel // 3))



# Som
pygame.mixer.music.load('Files/music.mp3')
pygame.mixer.music.play(-1)


config_vitoria = [
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1]
]
def referencia():

    margem = 50
    inicio_x = 1280 - tam_grade * (tam_cel // 3) - margem
    inicio_y = 720 - tam_grade * (tam_cel // 3) - margem

    # Desenha o tabuleiro de referência 9x9
    for x in range(tam_grade):
        for y in range(tam_grade):
            rect_x = inicio_x + x * (tam_cel // 3)
            rect_y = inicio_y + y * (tam_cel // 3)
            pygame.draw.rect(tela, cor_grade, (rect_x, rect_y, tam_cel // 3, tam_cel // 3), 1)

    # Chat fez essa parte junto a config_vitoria. Não percebi como ele acerta a matriz 3x3 dentro de uma 9x9
    # Desenha a configuração de vitória na área central da referência
    centro_inicio_x = inicio_x + 3 * (tam_cel // 3)
    centro_inicio_y = inicio_y + 3 * (tam_cel // 3)
    for x in range(3):
        for y in range(3):
            if config_vitoria[y][x] == 1:  # Desenha a peça apenas se corresponder à configuração de vitória
                rect_x = centro_inicio_x + x * (tam_cel // 3)
                rect_y = centro_inicio_y + y * (tam_cel // 3)
                tela.blit(imagem_peca_ref, (centro_inicio_x + x * (tam_cel // 3), centro_inicio_y + y * (tam_cel // 3)))


def colocar_pecas():
    for _ in range(9):
        while True:
            x, y = random.randint(0, tam_grade - 1), random.randint(0, tam_grade - 1)
            if tab[y][x] == 0:
                tab[y][x] = 1
                break


def desenhar():
    tela.blit(imagem_fundo, (0, 0))
    # Desenhar botões
    for x in range(tam_grade):
        pygame.draw.rect(tela, cor_btn, (x * tam_cel + larg_borda, 0, tam_cel, larg_borda))  # Top
        pygame.draw.rect(tela, cor_btn, (x * tam_cel + larg_borda, tam_tela - larg_borda, tam_cel, larg_borda))
    for y in range(tam_grade):
        pygame.draw.rect(tela, cor_btn, (0, y * tam_cel + larg_borda, larg_borda, tam_cel))  # Left
        pygame.draw.rect(tela, cor_btn, (tam_tela - larg_borda, y * tam_cel + larg_borda, larg_borda, tam_cel))

    for y in range(tam_grade):
        for x in range(tam_grade):
            rect = pygame.Rect(x * tam_cel + larg_borda, y * tam_cel + larg_borda, tam_cel, tam_cel)
            pygame.draw.rect(tela, cor_grade, rect, 1)
            if tab[y][x] == 1:
                tela.blit(imagem_peca, (x * tam_cel + larg_borda, y * tam_cel + larg_borda))


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
    if (x <= larg_borda and y <= larg_borda) or (
            x >= tam_tela - larg_borda and y >= tam_tela - larg_borda):  # Exclusão de quinas
        pass
    elif 0 < x < larg_borda < y < tam_tela - larg_borda:  # Botão esquerdo para linhas
        indice = (y - larg_borda) // tam_cel
        mover_linha(indice, 'esq')
        mover_coluna(indice, 'bai')
        pygame.mixer.Sound('Files/click_music.wav').play()
    elif tam_tela > x > tam_tela - larg_borda > y > larg_borda:  # Botão direito para linhas
        indice = (y - larg_borda) // tam_cel
        mover_linha(indice, 'dir')
        mover_coluna(indice, 'cim')
        pygame.mixer.Sound('Files/click_music.wav').play()
    elif 0 < y < larg_borda < x < tam_tela - larg_borda:  # Botão superior para colunas
        indice = (x - larg_borda) // tam_cel
        mover_coluna(indice, 'cim')
        mover_linha(indice, 'dir')
        pygame.mixer.Sound('Files/click_music.wav').play()
    elif tam_tela > y > tam_tela - larg_borda > x > larg_borda:  # Botão inferior para colunas
        indice = (x - larg_borda) // tam_cel
        mover_coluna(indice, 'bai')
        mover_linha(indice, 'esq')
        pygame.mixer.Sound('Files/click_music.wav').play()

        # fim chat


def calcular_pontuacao():
    pontos = 0
    inicio_central = 3
    for x in range(3):
        for y in range(3):
            # Supondo que a referência esteja no centro do tabuleiro principal
            if tab[inicio_central + y][inicio_central + x] == config_vitoria[y][x]:
                pontos += 1
    return pontos


def desenhar_barra_pontuacao(pontos):
    # Configurações da barra de pontuação
    cor_barra = (0, 255, 0)
    largura_total = 200
    altura = 20
    inicio_x = 1080  # Posição x onde a barra de pontuação começa
    inicio_y = 680  # Posição y onde a barra de pontuação começa

    # Calcula a largura da barra preenchida baseado nos pontos
    largura_preenchida = (largura_total / 9) * pontos

    # Desenha o contorno da barra de pontuação
    pygame.draw.rect(tela, cor_grade, (inicio_x, inicio_y, largura_total, altura), 2)
    # Desenha a barra preenchida
    pygame.draw.rect(tela, cor_barra, (inicio_x, inicio_y, largura_preenchida, altura))


def jogo():
    colocar_pecas()
    rodando = True
    pontos = 0  # Inicializa a pontuação
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                processa_clique(x, y)
                pontos = calcular_pontuacao()  # Atualiza a pontuação após cada clique

        desenhar()
        referencia()
        desenhar_barra_pontuacao(pontos)  # Desenha a barra de pontuação baseada nos pontos atuais

        if pontos == 9:  # Se todas as peças estão corretas
            print("Você venceu!")  # Ou pode adicionar uma mensagem na tela
            rodando = False

        pygame.display.flip()

    pygame.quit()


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    jogo()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
