import pygame
import sys
import time
import random

# Inicializando o Pygame
pygame.init()

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AMARELO = (255, 255, 0)

# Configurações da tela
largura, altura = 1280, 720
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Quiz Game')

# Definindo fontes
fonte_titulo = pygame.font.SysFont('Arial', 60)
fonte_botao = pygame.font.SysFont('Arial', 30)
fonte_pergunta = pygame.font.SysFont('Arial', 30)
fonte_opcao = pygame.font.SysFont('Arial', 25)
fonte_pontuacao = pygame.font.SysFont('Arial', 25)

# Configurações do jogo
tempo_limite = 30  # Segundos para responder cada pergunta
pontuacao = 0
respostas_consecutivas_corretas = 0
fase_atual = 1
perguntas_por_fase = 10
relogio = pygame.time.Clock()  # Controla o tempo

# Exemplo de perguntas (pode ser expandido ou carregado de um arquivo)
perguntas = [
    {"pergunta": "Qual a capital da França?", "opcoes": ["Paris", "Londres", "Berlim", "Roma"], "correta": 0},
    {"pergunta": "Qual o maior planeta do sistema solar?", "opcoes": ["Terra", "Marte", "Júpiter", "Saturno"], "correta": 2},
    # Adicione mais perguntas conforme necessário...
]

# Função para desenhar texto
def desenhar_texto(texto, fonte, cor, x, y):
    tela_texto = fonte.render(texto, True, cor)
    tela.blit(tela_texto, (x, y))

# Função para desenhar pontuação e tempo restante
def desenhar_pontuacao_e_tempo(pontuacao, tempo_restante):
    desenhar_texto(f"Pontuação: {pontuacao}", fonte_pontuacao, PRETO, 20, 20)
    desenhar_texto(f"Tempo: {tempo_restante:.1f}s", fonte_pontuacao, PRETO, largura - 200, 20)

# Função para criar os botões (com centralização de texto)
def criar_botao(texto, fonte, cor_texto, cor_fundo, x, y, largura, altura):
    pygame.draw.rect(tela, cor_fundo, (x, y, largura, altura))
    tela_texto = fonte.render(texto, True, cor_texto)
    texto_rect = tela_texto.get_rect(center=(x + largura // 2, y + altura // 2))
    tela.blit(tela_texto, texto_rect)
    return pygame.Rect(x, y, largura, altura)

# Função para exibir mensagem de tempo esgotado
def mostrar_tempo_esgotado():
    tela.fill(BRANCO)
    desenhar_texto("Tempo esgotado!", fonte_titulo, VERMELHO, largura // 2 - 150, altura // 2 - 50)
    desenhar_texto("Pressione Enter para voltar ao menu.", fonte_pergunta, PRETO, largura // 2 - 250, altura // 2 + 50)
    pygame.display.flip()

    # Esperar o usuário pressionar Enter
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:  # Tecla Enter
                    esperando = False

# Função para iniciar o jogo
def iniciar_jogo():
    global fase_atual, pontuacao, respostas_consecutivas_corretas
    rodando = True
    pergunta_atual = 0
    fase_atual = 1
    pontuacao = 0
    respostas_consecutivas_corretas = 0
    perguntas_da_fase = perguntas.copy()  # Embaralhar ou selecionar perguntas da fase

    while rodando:
        # Limpar tela
        tela.fill(BRANCO)

        # Configurar o tempo restante
        tempo_restante = tempo_limite  # Tempo inicial para cada pergunta

        while tempo_restante > 0 and rodando:
            # Atualizar o tempo restante
            tempo_decorrido = relogio.tick(60) / 1000  # Tempo decorrido em segundos
            tempo_restante -= tempo_decorrido

            # Desenhar a pontuação e o tempo restante
            desenhar_pontuacao_e_tempo(pontuacao, tempo_restante)

            # Verificar se a fase foi concluída
            if pergunta_atual >= perguntas_por_fase:
                desenhar_texto(f"Parabéns! Fase {fase_atual} concluída!", fonte_titulo, VERDE, largura // 2 - 200, altura // 2 - 50)
                fase_atual += 1
                pergunta_atual = 0
                if fase_atual > 5:  # Se já passou por 5 fases
                    desenhar_texto("Você concluiu o jogo!", fonte_titulo, VERMELHO, largura // 2 - 200, altura // 2 + 50)
                    pygame.display.flip()
                    time.sleep(3)
                    return

                # Exibir uma pausa antes de passar para a próxima fase
                pygame.display.flip()
                time.sleep(3)
                perguntas_da_fase = perguntas.copy()

            # Exibir a pergunta atual
            pergunta = perguntas_da_fase[pergunta_atual]
            desenhar_texto(f"Fase {fase_atual} - Pergunta {pergunta_atual + 1}", fonte_pergunta, PRETO, 50, 50)
            desenhar_texto(pergunta["pergunta"], fonte_pergunta, PRETO, 50, 100)

            # Exibir as opções
            botoes_opcoes = []
            for i, opcao in enumerate(pergunta["opcoes"]):
                botao = criar_botao(opcao, fonte_opcao, BRANCO, AZUL, 50, 200 + (i * 60), 400, 50)
                botoes_opcoes.append(botao)

            # Verificar eventos
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
                                if respostas_consecutivas_corretas == 5:
                                    pontuacao += 50  # Bônus por 5 respostas consecutivas
                            else:
                                respostas_consecutivas_corretas = 0
                            pergunta_atual += 1
            
            # Atualizar a tela
            pygame.display.flip()

        # Se o tempo acabar
        if tempo_restante <= 0:
            mostrar_tempo_esgotado()

# Função principal do menu
def menu_inicial():
    rodando = True
    while rodando:
        # Limpar tela
        tela.fill(BRANCO)

        # Título do menu
        desenhar_texto("Quiz Game", fonte_titulo, PRETO, largura // 2 - 150, 100)

        # Criando botões
        botao_novo_jogo = criar_botao("Novo Jogo", fonte_botao, BRANCO, AZUL, largura // 2 - 100, 250, 200, 50)
        botao_pontuacoes = criar_botao("Pontuações", fonte_botao, BRANCO, VERMELHO, largura // 2 - 100, 320, 200, 50)
        botao_opcoes = criar_botao("Opções", fonte_botao, BRANCO, VERDE, largura // 2 - 100, 390, 200, 50)

        # Detectar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_novo_jogo.collidepoint(evento.pos):
                    iniciar_jogo()  # Iniciar o jogo
                elif botao_pontuacoes.collidepoint(evento.pos):
                    print("Pontuações ainda não implementadas.")
                elif botao_opcoes.collidepoint(evento.pos):
                    print("Opções ainda não implementadas.")

        # Atualizar a tela
        pygame.display.flip()

# Rodar o menu inicial
menu_inicial()
pygame.quit()
