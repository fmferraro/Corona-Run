#Importando Bibliotecas necessárias para o jogo
import os
import sys
import pygame
from random import randint
from pygame import mixer

pygame.init()
mixer.init()

#Arquivos:
img_dir = os.path.join(os.path.dirname(__file__), 'Imagens')
som_dir = os.path.join(os.path.dirname(__file__), 'Sons')

#Superfície do jogo
LARGURA = 600
COMPRIMENTO = 600
tamanho_tela = (LARGURA, COMPRIMENTO)
superficie = pygame.display.set_mode(tamanho_tela)
pygame.display.set_caption("FMF Game")#Título da tela do jogo
CINZA=(127, 127, 127)  #Cor de fundo
FPS = 65


# Iniciar assets: 
police_largura = 200
police_comprimento = 100
tree_largura = 100
tree_comprimento = 100
player_largura = 100
player_comprimento = 207
oil_largura = 80
oil_comprimento = 80

assets = {}

assets['player_img'] = pygame.image.load(os.path.join(img_dir,'ferrari.png')).convert_alpha()
assets['player_img'] = pygame.transform.scale(assets['player_img'], (player_largura, player_comprimento))

assets['police_img'] = pygame.image.load(os.path.join(img_dir,'police.png')).convert_alpha()
assets['police_img'] = pygame.transform.scale(assets['police_img'], (police_largura, police_comprimento))

assets['oil_img'] = pygame.image.load(os.path.join(img_dir,'oil.png')).convert_alpha()
assets['oil_img'] = pygame.transform.scale(assets['oil_img'], (oil_largura, oil_comprimento))

assets['tree_img'] = pygame.image.load(os.path.join(img_dir, 'tree.png')).convert_alpha()
assets['tree_img'] = pygame.transform.scale(assets['tree_img'], (tree_largura, tree_comprimento))

assets['background_img'] = pygame.image.load(os.path.join(img_dir,'road.png')).convert()
assets['background_img'] = pygame.transform.scale(assets['background_img'], (LARGURA, COMPRIMENTO))


# Carregando sons do jogo: 
pygame.mixer.music.load(os.path.join(som_dir, "MusicaFundo.oga"))
pygame.mixer.music.set_volume(0.1)


#Classes do jogo

class Fundo_intro(pygame.sprite.Sprite):
    def __init__(self,texto1,texto2,texto3,texto4,texto5,texto6,texto7,texto8, cor_da_letra, tamanho_do_titulo,tamanho_da_instrucao, cor_fundo):
        tela_jogo2 = pygame.display.set_mode(tamanho_tela)
        tela_jogo2.fill(cor_fundo)
        self.fonte_texto1 = pygame.font.SysFont(None, tamanho_do_titulo)
        self.superficie1 = self.fonte_texto1.render(texto1, True, cor_da_letra)
        tela_jogo2.blit(self.superficie1, ((tela_jogo2.get_width()-self.superficie1.get_width())/2, 60))
        self.fonte_texto2 = pygame.font.SysFont(None, tamanho_do_titulo)
        self.superficie2 = self.fonte_texto2.render(texto2, True, cor_da_letra)
        tela_jogo2.blit(self.superficie2, ((tela_jogo2.get_width()-self.superficie2.get_width())/2, 120))
        self.fonte_texto3 = pygame.font.SysFont(None, tamanho_do_titulo)
        self.superficie3 = self.fonte_texto3.render(texto3, True, cor_da_letra)
        tela_jogo2.blit(self.superficie3, ((tela_jogo2.get_width()-self.superficie3.get_width())/2, 180))
        self.fonte_texto4 = pygame.font.SysFont(None, tamanho_da_instrucao)
        self.superficie4 = self.fonte_texto4.render(texto4, True, cor_da_letra)
        tela_jogo2.blit(self.superficie4, ((tela_jogo2.get_width()-self.superficie3.get_width())/2, 300))
        self.fonte_texto5 = pygame.font.SysFont(None, tamanho_da_instrucao)
        self.superficie5 = self.fonte_texto5.render(texto5, True, cor_da_letra)
        tela_jogo2.blit(self.superficie5, ((tela_jogo2.get_width()-self.superficie5.get_width())/2, 360))
        self.fonte_texto6 = pygame.font.SysFont(None, tamanho_da_instrucao)
        self.superficie6 = self.fonte_texto6.render(texto6, True, cor_da_letra)
        tela_jogo2.blit(self.superficie6, ((tela_jogo2.get_width()-self.superficie6.get_width())/2, 420))
        self.fonte_texto7 = pygame.font.SysFont(None, tamanho_da_instrucao)
        self.superficie7 = self.fonte_texto7.render(texto7, True, cor_da_letra)
        tela_jogo2.blit(self.superficie7, ((tela_jogo2.get_width()-self.superficie7.get_width())/2, 480))
        self.fonte_texto8 = pygame.font.SysFont(None, tamanho_da_instrucao)
        self.superficie8 = self.fonte_texto8.render(texto8, True, cor_da_letra)
        tela_jogo2.blit(self.superficie8, ((tela_jogo2.get_width()-self.superficie8.get_width())/2, 540))
        pygame.display.update()

class Fundo(pygame.sprite.Sprite):
    def __init__(self, assets):
        pygame.sprite.Sprite.__init__(self)
        self.image = assets['background_img']
        self.rect = self.image.get_rect()
        self.x_mov = 0

class Player(pygame.sprite.Sprite):
    def __init__ (self, groups, assets):
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['player_img']
        self.rect = self.image.get_rect()

        self.rect.x = 250
        self.rect.y = 400

        self.velocidade_player = 0.2
        self.delta_player =  {"esquerda":0, "direita":0}

        self.groups = groups
        self.assets = assets
    
    def update(self, delta_time):
        #self.rect.x += self.delta_player
        self.rect.x += (self.delta_player["direita"] - self.delta_player["esquerda"]) * self.velocidade_player * delta_time

        # Mantem o personagem dentro da tela
        if self.rect.right > 510:
            self.rect.right = 510
        if self.rect.left < 80:
            self.rect.left = 80

class Police(pygame.sprite.Sprite):
    def __init__(self, assets):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = assets['police_img']
        self.rect = self.image.get_rect()

        self.rect.x = randint(80, 320)
        self.rect.y = 0

        self.velocidade_police = 0.2

    def update(self, delta_time):
        largura, altura = pygame.display.get_surface().get_size()
        self.rect.y += self.velocidade_police * delta_time

        if self.rect.y > 2000:
            self.rect.y = 0
            self.rect.x = randint(80, 320)
            self.rect.y += self.velocidade_police * delta_time
        

class Oil(pygame.sprite.Sprite):
    def __init__(self, assets):
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['oil_img']
        self.rect = self.image.get_rect()

        self.rect.x = randint(80, 430)
        self.rect.y = 601

        self.velocidade_oil = 0.2

    def update(self, delta_time):
        largura, altura = pygame.display.get_surface().get_size()
        self.rect.y += self.velocidade_oil * delta_time

        if self.rect.y > 800:
            self.rect.y = 0
            self.rect.x = randint(80, 430)
            self.rect.y += self.velocidade_oil * delta_time

class Tree(pygame.sprite.Sprite):
    def __init__(self, assets):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = assets['tree_img']
        self.rect = self.image.get_rect()

        self.rect.x = randint(80, 430)
        self.rect.y = 701

        self.velocidade_tree = 0.2

    def update(self, delta_time):
        largura, altura = pygame.display.get_surface().get_size()
        self.rect.y += self.velocidade_tree * delta_time

        if self.rect.y > 1600:
            self.rect.y = 0
            self.rect.x = randint(80, 430)
            self.rect.y += self.velocidade_tree * delta_time
   



#Cores para o jogo
CINZA = (127, 127, 127)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# Criando grupos 
all_sprites = pygame.sprite.Group()
all_police = pygame.sprite.Group()
all_oil = pygame.sprite.Group()
all_tree = pygame.sprite.Group()

groups = {}
groups['all_sprites'] = all_sprites
groups['all_police'] = all_police
groups['all_oil'] = all_oil
groups['all_tree'] = all_tree

#Criando fundo, personagem, bala, monstros
fundo = Fundo(assets)
player = Player(groups, assets)
police = Police(assets)
oil = Oil(assets)
tree = Tree(assets)


#Adicionando sprites
all_sprites.add(player)
all_sprites.add(police)
all_sprites.add(oil)
all_sprites.add(tree)


all_police.add(police)
all_oil.add(oil)
all_tree.add(tree)

#Placar de tempo
font = pygame.font.SysFont("arial black", 25)
texto = font.render("Tempo: ", True, (255,255,255), (0, 0, 0))
pos_texto = texto.get_rect()
pos_texto.center = (55, 15) 
timer = 0
tempo_segundo = 0

# Fonte para a tela pausada
font_pause = pygame.font.SysFont("arial black", 40)

#Rodando a música de fundo
mixer.music.play(-1)

    
intro = Fundo_intro("Bem Vindo","ao","Corona Run","Vamos ver se você é um bom piloto...","Corra o maior tempo possível sem bater!","Caso encoste em um obstáculo, sua corrida acaba","Pressione DIREITA ou ESQUERDA para mover o carro","Pressione ENTER para continuar", (BRANCO), 80,30, (CINZA))


#Objeto para controle da atualizações de imagens
clock = pygame.time.Clock() 
FPS=60 #Velocidade que atualiza as imagens

RODANDO = 0
PAUSADO = 1

jogo = RODANDO

#Loop da tela inicial

Intro = True
while Intro:
    intro.__init__
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if keys[pygame.K_RETURN]:
            Intro = False
        elif event.type == pygame.QUIT:
            pygame.quit()

#Loop pricipal
JOGANDO = True
while JOGANDO:

    delta_time=clock.tick(FPS)

    #Eventos do jogo
    eventos=pygame.event.get()
        
    for evento in eventos:
                
        #Fecha o jogo
        if evento.type == pygame.QUIT or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE):
            pygame.quit() #Encerra a aplicação pygame
            sys.exit() #Sai pela rotina do sistema

        #Verifica se apertou alguma tecla
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT: #Controla o player
                player.delta_player["esquerda"] = 1
            if evento.key == pygame.K_RIGHT:
                player.delta_player["direita"] = 1

            if evento.key == pygame.K_p:#Pausa o jogo
                if jogo != PAUSADO:
                    mixer.music.pause()
                    pause = font_pause.render("PAUSE", True, PRETO, BRANCO)
                    superficie.blit(pause, ((superficie.get_width()-pause.get_width())/2, (superficie.get_height()-pause.get_height())/2))
                    jogo = PAUSADO
                else:
                    mixer.music.unpause()
                    jogo = RODANDO

            #Verifica se soltou alguma tecla
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT:
                player.delta_player["esquerda"] = 0
            if evento.key == pygame.K_RIGHT:
                player.delta_player["direita"] = 0
            
        #Posição do player
        #player.rect.x += (player.delta_player["direita"] - player.delta_player["esquerda"]) * player.velocidade_player * delta_time

    #Placar de tempo
    if timer<60 and jogo!= PAUSADO:
        timer += 1
    elif timer>=60 and jogo!= PAUSADO:
        tempo_segundo += 1
        texto = font.render("Tempo: "+str(tempo_segundo), True, (255,255,255), (0, 0, 0))
        timer = 0
                    
    if jogo == PAUSADO:
        pygame.display.flip()
        continue

    #Preenche a tela com a cor definida
    superficie.fill(PRETO)
            
            
    #Atualiza os sprites
    all_sprites.update(delta_time)

    #Colisões 
    hit_player_police = pygame.sprite.spritecollide(player, all_police, True)
    hit_player_oil = pygame.sprite.spritecollide(player, all_oil, True)
    hit_player_tree = pygame.sprite.spritecollide(player, all_tree, True)

    if len(hit_player_police) > 0 or len(hit_player_oil) > 0 or len(hit_player_tree) > 0: 
        print("hit")

            
    #Movimentação do fundo
    superficie.fill(PRETO)
    fundo.rect.x += 0.2
    if fundo.rect.right<0:
        fundo.rect.x += fundo.rect.width
    superficie.blit(fundo.image, fundo.rect)

    fundo.rect2 = fundo.rect.copy()
    fundo.rect2.x += fundo.rect2.width

    superficie.blit(fundo.image, fundo.rect2)

    #Rodando musica de fundo
    pygame.mixer.music.play(-1)
            
    #Desenhando os sprites
    all_sprites.draw(superficie)
            
    #Faz a atualização da tela
    pygame.display.flip()
    pygame.display.update()
