import pygame
import sys
import time
import json
import random

pygame.init()

# Cores e configurações
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AMARELO = (255, 255, 0)

largura, altura = 1280, 720
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Quiz Game')

# Fontes
fonte_titulo = pygame.font.SysFont('Arial', 60)
fonte_botao = pygame.font.SysFont('Arial', 30)
fonte_pergunta = pygame.font.SysFont('Arial', 30)
fonte_opcao = pygame.font.SysFont('Arial', 25)
fonte_pontuacao = pygame.font.SysFont('Arial', 25)

# Configurações de tempo e pontuação
tempo_limite = 30  
pontuacao = 0
respostas_consecutivas_corretas = 0
fase_atual = 1
perguntas_por_fase = 10
relogio = pygame.time.Clock()

# Função para carregar perguntas de um arquivo JSON
def carregar_perguntas(caminho):
    with open(caminho, 'r', encoding='utf-8') as arquivo:
        return json.load(arquivo)

# Carregar perguntas
try:
    perguntas_dados = carregar_perguntas('perguntas.json')
except FileNotFoundError:
    print("Arquivo perguntas.json não encontrado!")
    sys.exit()
except UnicodeDecodeError:
    print("Erro de decodificação de caracteres no arquivo!")
    sys.exit()

perguntas_por_fase = perguntas_dados['fases']

def desenhar_texto(texto, fonte, cor, x, y):
    tela_texto = fonte.render(texto, True, cor)
    tela.blit(tela_texto, (x, y))

def desenhar_pontuacao_e_tempo(pontuacao, tempo_restante):
    desenhar_texto(f"Pontuação: {pontuacao}", fonte_pontuacao, PRETO, 20, 20)
    desenhar_texto(f"Tempo: {tempo_restante:.1f}s", fonte_pontuacao, PRETO, largura - 200, 20)

def criar_botao(texto, fonte, cor_texto, cor_fundo, x, y, largura, altura):
    pygame.draw.rect(tela, cor_fundo, (x, y, largura, altura))
    tela_texto = fonte.render(texto, True, cor_texto)
    texto_rect = tela_texto.get_rect(center=(x + largura // 2, y + altura // 2))
    tela.blit(tela_texto, texto_rect)
    return pygame.Rect(x, y, largura, altura)

def mostrar_tempo_esgotado():
    tela.fill(BRANCO)
    desenhar_texto("Tempo esgotado!", fonte_titulo, VERMELHO, largura // 2 - 150, altura // 2 - 50)
    desenhar_texto("Pressione Enter para voltar ao menu.", fonte_botao, PRETO, largura // 2 - 250, altura // 2 + 50)
    pygame.display.flip()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    esperando = False

def iniciar_jogo():
    global fase_atual, pontuacao, respostas_consecutivas_corretas
    rodando = True
    pergunta_atual = 0
    fase_atual = 1
    pontuacao = 0
    respostas_consecutivas_corretas = 0
    perguntas_da_fase = perguntas_por_fase[fase_atual - 1]['perguntas']
    random.shuffle(perguntas_da_fase)
    tempo_restante = tempo_limite

    while rodando:
        tela.fill(BRANCO)

        tempo_decorrido = relogio.tick(60) / 1000  
        tempo_restante -= tempo_decorrido

        desenhar_pontuacao_e_tempo(pontuacao, tempo_restante)

        if pergunta_atual >= len(perguntas_da_fase):
            desenhar_texto(f"Parabéns! Fase {fase_atual} concluída!", fonte_titulo, VERDE, largura // 2 - 200, altura // 2 - 50)
            fase_atual += 1
            if fase_atual > len(perguntas_por_fase):
                desenhar_texto("Você concluiu o jogo!", fonte_titulo, VERMELHO, largura // 2 - 200, altura // 2 + 50)
                pygame.display.flip()
                time.sleep(3)
                return

            pygame.display.flip()
            time.sleep(3)
            perguntas_da_fase = perguntas_por_fase[fase_atual - 1]['perguntas']
            random.shuffle(perguntas_da_fase)
            pergunta_atual = 0

        pergunta = perguntas_da_fase[pergunta_atual]
        desenhar_texto(f"Fase {fase_atual} - Pergunta {pergunta_atual + 1}", fonte_pergunta, PRETO, 50, 50)
        desenhar_texto(pergunta["pergunta"], fonte_pergunta, PRETO, 50, 100)

        botoes_opcoes = []
        for i, opcao in enumerate(pergunta["opcoes"]):
            botao = criar_botao(opcao, fonte_opcao, BRANCO, AZUL, 50, 200 + (i * 60), 400, 50)
            botoes_opcoes.append(botao)

        if tempo_restante <= 0:
            mostrar_tempo_esgotado()
            return  

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                sys.exit()
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for i, botao in enumerate(botoes_opcoes):
                    if botao.collidepoint(evento.pos):
                        if i == pergunta["correta"]:
                            pontuacao += 10
                            respostas_consecutivas_corretas += 1
                        else:
                            respostas_consecutivas_corretas = 0
                        pergunta_atual += 1
                        
                        #reinicia cronometro
                        tempo_restante = tempo_limite
                        break

        pygame.display.flip()

def mostrar_estatisticas():
    # Aqui você pode implementar a lógica para mostrar as estatísticas dos jogadores
    tela.fill(BRANCO)
    desenhar_texto("Estatísticas de Pontuação", fonte_titulo, AZUL, largura // 2 - 200, altura // 2 - 200)
    # Exemplo de estatísticas, você pode modificar conforme necessário
    desenhar_texto("Jogador 1: 100 pontos", fonte_botao, PRETO, largura // 2 - 100, altura // 2 - 100)
    desenhar_texto("Jogador 2: 200 pontos", fonte_botao, PRETO, largura // 2 - 100, altura // 2 - 50)
    desenhar_texto("Pressione Enter para voltar ao menu.", fonte_botao, PRETO, largura // 2 - 250, altura // 2 + 50)
    pygame.display.flip()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    esperando = False

def mostrar_sobre():
    tela.fill(BRANCO)
    desenhar_texto("Sobre o Jogo", fonte_titulo, AZUL, largura // 2 - 200, altura // 2 - 200)
    desenhar_texto("Este é um jogo de quiz!", fonte_botao, PRETO, largura // 2 - 100, altura // 2 - 100)
    desenhar_texto("Desafie seus conhecimentos!", fonte_botao, PRETO, largura // 2 - 100, altura // 2 - 50)
    desenhar_texto("Pressione Enter para voltar ao menu.", fonte_botao, PRETO, largura // 2 - 250, altura // 2 + 50)
    pygame.display.flip()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    esperando = False

# Loop principal
while True:
    tela.fill(BRANCO)
    desenhar_texto("Quiz Game", fonte_titulo, AZUL, largura // 2 - 150, altura // 2 - 200)

    # Criar botões do menu
    botao_jogar = criar_botao("Jogar", fonte_botao, BRANCO, VERDE, largura // 2 - 100, altura // 2 - 50, 200, 50)
    botao_estatisticas = criar_botao("Estatísticas", fonte_botao, BRANCO, AMARELO, largura // 2 - 100, altura // 2 + 10, 200, 50)
    botao_sobre = criar_botao("Sobre", fonte_botao, BRANCO, VERMELHO, largura // 2 - 100, altura // 2 + 70, 200, 50)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if botao_jogar.collidepoint(evento.pos):
                iniciar_jogo()
            elif botao_estatisticas.collidepoint(evento.pos):
                mostrar_estatisticas()
            elif botao_sobre.collidepoint(evento.pos):
                mostrar_sobre()

    pygame.display.flip()
