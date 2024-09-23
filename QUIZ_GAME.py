import pygame
import sys

# Inicializando o Pygame
pygame.init()

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)

# Configurações da tela
largura, altura = 1280, 720
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Quiz - Menu Inicial')

# Definindo fontes
fonte_titulo = pygame.font.SysFont('Arial', 60)
fonte_botao = pygame.font.SysFont('Arial', 30)

# Função para desenhar texto
def desenhar_texto(texto, fonte, cor, x, y):
    tela_texto = fonte.render(texto, True, cor)
    tela.blit(tela_texto, (x, y))

# Função para criar os botões (com centralização de texto)
def criar_botao(texto, fonte, cor_texto, cor_fundo, x, y, largura, altura):
    # Desenha o retângulo do botão
    pygame.draw.rect(tela, cor_fundo, (x, y, largura, altura))
    
    # Renderiza o texto do botão
    tela_texto = fonte.render(texto, True, cor_texto)
    texto_rect = tela_texto.get_rect(center=(x + largura // 2, y + altura // 2))
    
    # Desenha o texto centralizado dentro do botão
    tela.blit(tela_texto, texto_rect)

    # Retorna o retângulo do botão para detecção de clique
    return pygame.Rect(x, y, largura, altura)

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
                    print("Novo Jogo foi clicado!")
                    # Chamar a função de iniciar o jogo (a ser implementada)
                elif botao_pontuacoes.collidepoint(evento.pos):
                    print("Pontuações foi clicado!")
                    # Chamar a função de mostrar pontuações (a ser implementada)
                elif botao_opcoes.collidepoint(evento.pos):
                    print("Opções foi clicado!")
                    # Chamar a função de opções (a ser implementada)

        # Atualizar a tela
        pygame.display.flip()

# Iniciar o menu inicial
menu_inicial()
