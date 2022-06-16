# -*- coding: UTF-8 -*-
#@tobias wendl
#@Quentin Guer

import pygame
from pygame import *
import Button
from Button import *
import time
import IP_perso
import ping3 as ping
import socket

HOST = "192.168.43.18"
PORT = 65432


class Piece:

    def __init__(self, xPos, yPos, type):

        self.player = 0  # 0-> n appartient a aucun joueur
        self.pos = (xPos, yPos)
        self.corpse = []  # corps du navire
        self.listRect = []
        self.size = 0
        self.type = type  # string qui définit le type de la piece
        self.frame = False
        self.collision = False
        self.placed = False
        self.sunk = False

        # permet de compter le nombre de pieces d'un type donné
        # attribut utilisé lors du placement des pieces
        self.counter = 1
        # on init la taille en fct du type
        if type == "porte avion":
            self.size = 5

        elif type == "croiseur":
            self.size = 4

        elif type == "contre torpilleur":
            self.size = 3
            self.counter = 2

        elif type == "torpilleur":
            self.size = 2

        # on init la liste qui sert de corps au navire
        # on init à 0
        # 0 représente gris
        # 1 représente rouge --> navire touché
        for i in range(self.size):
            self.corpse.append(0)

    def display(self, window):
        """permet d'afficher les pièces"""
        font = pygame.font.SysFont("comicsans", 30, True)
        color = (135, 138, 136)
        xPos, yPos = self.pos[0], self.pos[1]
        for i in range(self.size):
            ship = pygame.Rect(xPos, yPos, 30, 30)
            self.listRect.append(ship)
            pygame.draw.rect(window, color, ship)
            xPos += 31
        var_text = str(self.type + " : x" + str(self.counter))
        text = font.render(var_text, 1, (255, 255, 255))
        window.blit(text, (self.pos[0], self.pos[1] - 50))

    def check_click(self, window):
        """permet de tester si une piece a ete cliqué"""
        mouseX, mouseY = pygame.mouse.get_pos()
        color = (53, 16, 235)
        for i in range(len(self.listRect)):
            if self.listRect[i].collidepoint((mouseX, mouseY)):
                self.collision = True
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        print("piece clicked")
                        self.frame = True
        if self.frame:
            # définit le cadre à dessiner autour d'une certaine pièce
            rect_frame = pygame.Rect(self.pos[0], self.pos[1], self.size * 30 + self.size, 32)
            # place un cadre autour de la piece cliquée
            pygame.draw.rect(window, color, rect_frame, 2)


class Grid:
    def __init__(self, xPos, yPos):
        self.size = (10, 10)
        self.grid = []
        for i in range(self.size[0]):
            self.grid.append([])
            for j in range(self.size[1]):
                self.grid[i].append(0)
        self.pos = (xPos, yPos)
        self.listRect = []

    def display(self, window):
        """affichage de la grille de jeu
            Les 0 représentent une case vide
            Les 1 représente une case avec un navire
            Les 2 représentent une case vide touchée
            Les 3 representent une case avec un navire touchée"""
        self.listRect = []
        q = 0
        yPos = self.pos[1]
        for j in range(self.size[0]):
            xPos = self.pos[0]
            for k in range(self.size[1]):
                switcher = {
                    0: (255, 255, 255),
                    1: (135, 138, 136),
                    2: (0, 0, 0),
                    3: (255, 0, 0)
                }
                self.listRect.append(pygame.Rect(xPos, yPos, 30, 30))
                color = switcher.get(self.grid[j][k], (0, 255, 0))
                pygame.draw.rect(window, color, self.listRect[q])
                xPos += 31
                q += 1
            yPos += 31
        return color

    def placement(self, window, size, rotate):
        """permet de placer les navires sur la grille"""
        mouseX, mouseY = pygame.mouse.get_pos()
        placed = False
        for i in range(len(self.listRect)):
            if self.listRect[i].collidepoint((mouseX, mouseY)):
                # on sauvegarde la variable i en utilisant une variable m
                m = i
                # si l'on souhaite placer les navires à l'horizontale
                # -->sélecteur à l'horizontale
                if rotate == False:
                    # boucle for qui permet d'afficher un 'sélecteur' sur la grille
                    for j in range(size):
                        # on verfifie que la zone sélectionnée se situe à l'intérieur de la grille
                        if m < len(self.listRect):
                            pygame.draw.rect(window, (59, 199, 44), self.listRect[m], 2)
                            m += 1
                        # si on se situe en dehors de la grille --> affichage de la pièce sur les dernières cases dispo
                        else:
                            pygame.draw.rect(window, (59, 199, 44), self.listRect[m - size], 2)
                            m -= size - 1
                # si l'on souhaite placer les navires à la verticale
                # sélecteur à la verticale
                if rotate:
                    # boucle for qui permet d'afficher un 'sélecteur' sur la grille
                    for j in range(size):
                        # on vérifie que la zone sélectionnée se situe à l'intérieur de la grille
                        if m + self.size[0] < len(self.listRect) + self.size[0]:
                            pygame.draw.rect(window, (59, 199, 44), self.listRect[m], 2)
                            m += self.size[0]
                        # si on se situe en dehors de la grille --> affichage de la pièce sur les dernières cases dispo
                        else:
                            pygame.draw.rect(window, (59, 199, 44), self.listRect[m - self.size[0] * size], 2)
                            m -= self.size[0] * size - self.size[0]

                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        # la boucle for suivante permet de changer la couleur de tous les rect sélectionnés
                        # ex: torpilleur sélectionné --> 2 cases coloriées
                        # cad. placer les navires
                        for l in range(size):
                            # on vérifie que la zone sélectionnée se situe dans la grille
                            # il faut également vérifier l'orientation du navire
                            # si rotate == False --> navire à l'horizontale
                            # si rotate == True --> navire à la verticale

                            # positionnement pour navire à l'horizontale
                            if i < len(self.listRect) and rotate == False:
                                j = i // 10
                                k = i % 10
                                # on vérifie que les cases sélectionnées ne sont pas encore utilisées
                                if self.grid[j][k] == 0:
                                    self.grid[j][k] = 1
                                    print(self.grid)
                                    i += 1
                                    placed = True
                            else:
                                if rotate == False:
                                    j = (i - size) // 10
                                    k = (i - size) % 10
                                    if self.grid[j][k] == 0:
                                        self.grid[j][k] = 1
                                        print(self.grid)
                                        i -= size - 1
                                        placed = True

                            # positionnement pour navire à la verticale
                            if i + self.size[0] < len(self.listRect) + self.size[0] and rotate == True:
                                j = i // 10
                                k = i % 10
                                # on vérifie que les cases sélectionnées ne sont pas encore utilisées
                                if self.grid[j][k] == 0:
                                    self.grid[j][k] = 1
                                    print(self.grid)
                                    i += self.size[0]
                                    placed = True
                            else:
                                if rotate == True:
                                    j = (i - self.size[0] * size) // 10
                                    k = (i - self.size[0] * size) % 10
                                    if self.grid[j][k] == 0:
                                        self.grid[j][k] = 1
                                        print(self.grid)
                                        i -= self.size[0] * size - self.size[0]
                                        placed = True
                        if placed:
                            return True


def window_refresh(window):
    bg_image = pygame.image.load('img/blue.jpg')
    window.blit(bg_image, (0, 0))


def window_init():
    # initialisation pygame
    pygame.init()
    window = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("THE NAVAL BATTLE")
    window_refresh(window)
    return window


def Button_creation():
    """creation des bouttons"""
    button1 = Button('Play', 200, 40, (290, 400), 5)
    button2 = Button('How to play', 200, 40, (290, 470), 5)
    button3 = Button('Back to menu', 200, 40, (290, 540), 5)
    button4 = Button('Ready', 200, 40, (290, 600), 5)
    button5 = Button('Back to menu', 200, 40, (290, 670), 5)
    return button1, button2, button3, button4, button5


def grid_creation(xPos, yPos):
    """creation de la grille"""
    grid = Grid(xPos, yPos)
    return grid


def piece_creation(xPos, yPos, type):
    piece = Piece(xPos, yPos, type)
    return piece


def connection(min=0, max=255):
    IP = IP_perso.get_ip()
    print("mon IP est : %s" % (IP))
    list_IP = IP_perso.list_host(IP, min, max)
    print("la liste des hosts possible est : \n %s" % (list_IP))
    return list_IP


def clientfct(list_host):
    host_connect = ""
    conversation = True
    Connection = False
    mdp = "Test-Serveur"
    # on teste toutes les IP de la liste pour voir lesquels existent
    for host in list_host:
        test = ping.ping(host)

        if test == 0:  # 0 = connection echoue
            print("appareil : %s connection echoue" % (host))
        else:
            # une fois qu'on trouve un appareil connecte au reseau
            # on test si son port de connection special est ouvert
            print("appareil : %s connection reussi: <%s>" % (host, repr(test)))
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            destination = (host, 65432)
            error_connect = test_socket.connect_ex(destination)

            if error_connect == 0:
                print("   le port : 65432 est ouvert")
                try:
                    # si le port est ouvert on envoie un message de verification
                    # est on attend la reponse du serveur
                    # si le serveur nous repond que c'est bon on arrete la boucle
                    # et on passe en mode communication avec ce serveur
                    print("Test envoie du message de verification d'application")
                    test_socket.sendall(mdp.encode("utf-8"))
                    binverif = test_socket.recv(1024)
                    verif = binverif.decode("utf-8")
                    print(verif)
                    if verif == "ok":
                        Connection = True
                        host_connect = host
                        break
                except Exception as e:
                    print("erreur dans l'envoie du message \n -> erreur : %s" % (e))
            else:
                print("   le port : 65432 est pas ouvert")
    if Connection == False:
        # si on trouve aucun serveur alors on devient un serveur
        print("server_echo")
        # server_echo()
    """
    else:
        # message_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # newdestination = (host_connect, 65432)
        try:
            # on demande a l'utilisateur d'ecrire un message 
            # puis on l'encode en binaire
            # puis en l'envoie et on attend la reponse du serveur
            # qu'on decode et qu'on ecrit
            while conversation:
                message = input("tapez votre message\n")
                if message == "stop":
                    conversation = False
                try:
                    print("------Envoie du message-------")
                    # message_socket.sendall(message.encode("utf-8"))
                    test_socket.sendall(message.encode("utf-8"))
                    data = test_socket.recv(1024).decode("utf-8")
                    print("message recu : %s" % (data))
                    if data == "stop":
                        conversation = False
                        test_socket.sendall("stop".encode("utf-8"))
                except Exception as e:
                    print("erreur dans l'envoie du message \n -> erreur : %s" % (e))
                    conversation = False
        except Exception as e:
            print("erreur de connection avec l'hote \n -> erreur : %s" % (e))
        """
    return test_socket, Connection


def message(socket, message):
    print("socket = %s" % (socket))
    print("ENTREE DANS MESSAGE")

    socket.sendall(message.encode("utf-8"))
    # print("---test---\nsocket = %s et messge = %s \n---fin test ---"%(socket,message))
    binrecu = socket.recv(1024)
    # binrecu = "touche".encode("utf-8")
    recu = binrecu.decode("utf-8")
    print("reception %s" % recu)
    return recu


def victoire(socket):
    message(socket, "WIN:10")


def recep(socket, listRect):
    binrecu = socket.recv(1024).decode("utf-8")
    ACR = False
    print("ENTREE DANS RECEPTION \n message recu = %s" % (binrecu))
    if not binrecu:
        j = 0
        k = 0
        tir = False
    elif binrecu == "Bien recu":
        j = 1
        k = 1
        tir = False
        ACR = True
    else:
        tir = True
        print("reception =  %s" % (binrecu))
        msg = binrecu.split(":")
        i = int(msg[1])
        j = i // 10
        k = i % 10
        print("reception i = %s j = %s k = %s" % (i, j, k))
        if listRect[j][k] == 0:
            msg = "rate : %s" % (i)
            socket.sendall(msg.encode("utf-8"))
            print("---envoie rate")
        elif listRect[j][k] == 1:
            msg = "touche : %s" % (i)
            socket.sendall(msg.encode("utf-8"))
            print("---envoie touche")
    return j, k, tir, ACR


def server():
    print(f"server_echo: BEGIN")
    bLoop1 = True
    client = False
    while bLoop1:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            prise = socket.create_server((HOST, PORT))  # on ouvre le port de communication special
            print(f"server_echo: (listen)")
            s.listen()  # on attend que qqln ce connecte
            conn, addr = s.accept()  # on accept ca connection
            # conn = nouvelle socket pouvant etre utilise pour envoye et recevoir des message
            # addr = liens avec la socket de l'autre cote
            with prise:
                bLoop1 = False
                # on verifie que c'est bien notre application
                data = prise.recv(1024)
                sData = data.decode('utf-8')
                print(f"server_echo: Received {sData}")
                if sData == 'Test-Serveur':
                    verif = "ok"
                    prise.sendall(verif.encode("utf-8"))
                    print(f"server_echo: Connected by")
                    # on attend les message de l'utilisateur on le decode, l'ecrit
                    # l'interpret, et on le revoie
                    client = True
                else:
                    refus = "Le message d'autentification n'est pas le bon"
                    print(refus)
                    prise.sendall(refus.encode("utf-8"))
                print(f"server_echo: loop ended")
            print(f"server_echo: connexion closed")
        print(f"server_echo: ...")
    print(f"server_echo: END")
    return prise, client


def tir(sock, i, cmpt_touche):
    recu = message(sock, "tir : %s" % (i))
    print("--- envoie tir en %s " % (i))
    if recu == "touche : %i" % (i):
        cmpt_touche += 1
    if cmpt_touche <= 16:
        sock.sendall("Bien recu".encode("utf-8"))
        print("---envoie   Bien recu")
        print("compteur = %s" % (cmpt_touche))

    elif cmpt_touche >= 17:
        sock.sendall("WIN".encode("utf-8"))
        print("---envoie    WIN")
    return recu, cmpt_touche


def main_NavalBattle():
    """fonction main du jeu naval battle"""

    client = False
    Connect = False
    # attribution de la variable window
    window = window_init()

    # intialisation de la fenetre
    window_init()

    # creation du boutton de retour au menu
    button1, button2, button3, button4, button5 = Button_creation()

    # creation des grilles
    # gridA --> grille de l'utilisateur
    # gridB --> grille du joueur adverse
    gridA = grid_creation(50, 200)
    gridB = grid_creation(450, 200)

    # creation des pieces avec l'utilisation de la fonction piece_creation
    torpilleur = piece_creation(400, 200, 'torpilleur')
    contre_torpilleur = piece_creation(400, 300, 'contre torpilleur')
    croiseur = piece_creation(400, 400, 'croiseur')
    porte_avion = piece_creation(400, 500, 'porte avion')

    # définition de quelques booléens
    run = True
    menu = True
    play = False
    placement = True
    game = False
    rotate = False

    # définition de la variable clock
    # peut être utilisée pour gérer les FPS
    clock = pygame.time.Clock()

    # variable utilisée pour la méthode placement de la classe Grid
    size = 0

    # loading images
    logo = pygame.image.load('img/logoNV.PNG')
    placeShip = pygame.image.load('img/PlaceShip.PNG')

    # début de la boucle principale
    while run:
        # début de la boucle menu
        while menu:
            cmpt_touche = 0
            message_recu = ""
            # refresh de la fenetre à chaque début de boucle
            window_refresh(window)

            # affichage du logo
            window.blit(logo, (245, 70))

            # affichage des bouttons sur la fenetre
            button1.draw(window)
            button2.draw(window)
            button3.draw(window)

            # test si les bouttons ont été cliqués + définition des actions à effectué si bouttons cliqué

            if button1.pressed == True:
                print("Play")
                time.sleep(0.2)
                button1.pressed = False
                play = True
                placement = True
                menu = False
                fin = False

            if button2.pressed == True:
                print("how to play")
                time.sleep(0.2)

            if button3.pressed == True:
                print("back to main menu")
                time.sleep(0.2)
                button3.pressed = False
                run = False
                menu = False

            # permet à l'utilisateur de quitter le menu et le jeu
            # le renvoi sur le menu principal
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    menu = False

            # mise à jour de la fenetre
            pygame.display.update()

        # début de la boucle de jeu
        while play:
            compteur_tour = 0
            # Connect = True
            # sock = 42
            turn = 2
            # list_IP = connection(15,20)
            # socketsock, Connect = clientfct(list_IP)
            debug_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_connection = debug_socket.connect_ex((HOST, PORT))
            # mettre un reset de la grille ici
            # creation des grilles
            # gridA --> grille de l'utilisateur
            # gridB --> grille du joueur adverse
            gridA = grid_creation(50, 200)
            gridB = grid_creation(450, 200)

            # creation des pieces avec l'utilisation de la fonction piece_creation
            torpilleur = piece_creation(400, 200, 'torpilleur')
            contre_torpilleur = piece_creation(400, 300, 'contre torpilleur')
            croiseur = piece_creation(400, 400, 'croiseur')
            porte_avion = piece_creation(400, 500, 'porte avion')

            if test_connection == 0:
                print("Test envoie du message de verification d'application")
                debug_socket.sendall("Test-Serveur".encode("utf-8"))
                binverif = debug_socket.recv(1024).decode("utf-8")
                if binverif == "ok":
                    Connect = True
                    sock = debug_socket
            if not Connect:
                prise = socket.create_server((HOST, PORT))  # on ouvre le port de communication special
                prise.listen()
                sock, addresse = prise.accept()
                données = sock.recv(1024).decode("utf-8")
                if données == "Test-Serveur":
                    sock.sendall("ok".encode("utf-8"))
                    client = True
                    turn = 1
            if client == True or Connect == True:
                while placement:
                    win = False
                    # refresh de la fenetre à chaque début de boucle
                    window_refresh(window)

                    # on définit une variable qui représente la touche pressée.
                    keys = pygame.key.get_pressed()

                    # affichage de l'image contenant le texte 'placez vos navires'
                    window.blit(placeShip, (110, 0))

                    # affichage des bouttons 'ready' et 'retour au menu'
                    button4.draw(window)
                    button5.draw(window)

                    # affichage des pieces sur l'ecran
                    torpilleur.display(window)
                    contre_torpilleur.display(window)
                    croiseur.display(window)
                    porte_avion.display(window)

                    # verifier si on clique les pieces
                    torpilleur.check_click(window)
                    contre_torpilleur.check_click(window)
                    croiseur.check_click(window)
                    porte_avion.check_click(window)

                    # si celle-ci sont cliquées et n'ont pas encore été placées --> pièce sélectionnée
                    if torpilleur.frame and torpilleur.collision and torpilleur.counter > 0:
                        size = 2
                        contre_torpilleur.frame = False
                        croiseur.frame = False
                        porte_avion.frame = False
                        torpilleur.collision = False

                    # on teste si l'on peut encore placer la piece ou si elle se situe déjà sur la grille
                    if size == 2 and torpilleur.counter == 0:
                        size = 0

                    if contre_torpilleur.frame and contre_torpilleur.collision:
                        size = 3
                        torpilleur.frame = False
                        croiseur.frame = False
                        porte_avion.frame = False
                        contre_torpilleur.collision = False

                    if size == 3 and contre_torpilleur.counter == 0:
                        size = 0

                    if croiseur.frame and croiseur.collision:
                        size = 4
                        torpilleur.frame = False
                        contre_torpilleur.frame = False
                        porte_avion.frame = False
                        croiseur.collision = False

                    if size == 4 and croiseur.counter == 0:
                        size = 0

                    if porte_avion.frame and porte_avion.collision:
                        size = 5
                        torpilleur.frame = False
                        contre_torpilleur.frame = False
                        croiseur.frame = False
                        porte_avion.collision = False

                    if size == 5 and porte_avion.counter == 0:
                        size = 0

                    # affichage de la grille de jeu
                    gridA.display(window)

                    if keys[pygame.K_r] and rotate == False:
                        print('rotate')
                        time.sleep(0.1)
                        rotate = True
                    elif keys[pygame.K_r] and rotate == True:
                        print('rotate')
                        time.sleep(0.1)
                        rotate = False
                    placed = gridA.placement(window, size, rotate)

                    # si les pièces sont placées, on met à jour le compteur
                    # compteur --> nbre de pièces du même type encore disponibles
                    if placed:
                        if size == 2:
                            torpilleur.placed = True
                            torpilleur.counter -= 1
                        if size == 3:
                            contre_torpilleur.placed = True
                            contre_torpilleur.counter -= 1
                        if size == 4:
                            croiseur.placed = True
                            croiseur.counter -= 1
                        if size == 5:
                            porte_avion.placed = True
                            porte_avion.counter -= 1

                    # mise à jour de la fenetre
                    pygame.display.update()

                    # reinitialisation de la liste contenant les rectangle de la grille A
                    # évite un dépassement --> index <= 100
                    gridA.listRect = []

                    # on add tous les counter des pièces pour verifier que l'on peut lancer le jeu
                    counter = torpilleur.counter + contre_torpilleur.counter + croiseur.counter + porte_avion.counter

                    # button ready
                    if button4.pressed == True:
                        print("ready")
                        time.sleep(0.2)
                        button4.pressed = False
                        # on verifie que tous les navires sont posés avant de lancer le jeu
                        if counter == 0:
                            print("you can play")
                            placement = False
                            game = True
                            menu = False
                        else:
                            print("place all your ships")

                    # button back to menu
                    # permet de retourner au menu du jeu
                    if button5.pressed == True:
                        print("back to menu")
                        time.sleep(0.2)
                        button5.pressed = False
                        play = False
                        placement = False
                        menu = True

                    # permet à l'utilisateur de retourner au menu du jeu
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            play = False
                            placement = False
                            menu = True

                    # 60 fps
                    clock.tick(60)

                # début de la boucle du jeu après placement des navires
                while game:
                    shoot = False
                    font = pygame.font.Font(None, 50)
                    # refresh de la fenetre
                    window_refresh(window)
                    message_recu = ""

                    #colors
                    grey = (50, 50, 50)

                    # affichage de la grille de jeu
                    gridA.display(window)
                    gridB.display(window)

                    #affichage des noms des joueurs en dessous de la grille
                    textName1 = font.render("Vous", 1, grey)
                    textName2 = font.render("Adversaire", 1, grey)

                    window.blit(textName1, (100, 550))
                    window.blit(textName2, (550, 550))

                    # mise à jour de la fenetre
                    mouseX, mouseY = pygame.mouse.get_pos()
                    # print("souris en : %s %s"%(mouseX,mouseY))
                    if turn == 1:
                        #indique au joueur que c'est à lui de jouer
                        textTurn = font.render("A VOUS DE JOUER", 1, grey)
                        for i in range(len(gridB.listRect)):
                            message_recu = ""
                            if gridB.listRect[i].collidepoint((mouseX, mouseY)):
                                pygame.draw.rect(window, (59, 199, 44), gridB.listRect[i], 2)
                                # print("collision")
                                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                                    # print("clique")
                                    j = i // 10
                                    k = i % 10
                                    print("j = %s k = %s" % (j, k))
                                    # on vérifie que les cases sélectionnées ne sont pas encore utilisées
                                    if gridB.grid[j][k] == 0:
                                        message_recu, cmpt_touche = tir(sock, i, cmpt_touche)
                                        print("message recu :" + message_recu)
                                        turn = 2
                                        # time.sleep(0.5)
                                        if message_recu == "Bien recu":
                                            x = 1
                                        else:
                                            message_recu = message_recu.split(":")
                                            print("message recu apres split :", message_recu)
                                            if message_recu[0] == "touche ":
                                                #etat du tir affiché sur l'écran
                                                #ici on affiche touché si le tir a atteint sa cible
                                                textShotState = font.render("Touche", 1, grey)
                                                gridB.grid[j][k] = 3
                                                # print("navire touche")
                                            elif message_recu[0] == "rate ":
                                                textShotState = font.render("Manque", 1, grey)
                                                gridB.grid[j][k] = 2

                            if message_recu == "WIN":
                                fin = True
                                win = False
                            else:
                                x = 1
                        window.blit(textShotState, (350, 150))
                    if turn == 2:
                        textTurn = font.render("AU TOUR DE L'ADVERSAIRE", 1, grey)
                        j, k, shoot, ACR = recep(sock, gridA.grid)
                        print(gridA.grid)
                        if gridA.grid[j][k] == 0 and shoot:
                            gridA.grid[j][k] = 2
                            print(gridA.grid)
                        elif gridA.grid[j][k] == 1 and shoot:
                            gridA.grid[j][k] = 3
                            print(gridA.grid)
                        if ACR:
                            turn = 1
                    window.blit(textTurn, (350, 50))
                    # print ("turn = %s"%(turn))
                    if cmpt_touche >= 17:
                        win = True
                        fin = True
                    pygame.display.update()
                    # permet à l'utilisateur de quitter le jeu --> retour au menu principal
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            game = False
                            play = False
                            placement = False
                            menu = True
                    # reinitialisation de la liste contenant les rectangle de la grille A et de la grille B
                    # évite un dépassement --> index <= 100

                    gridA.display(window)
                    gridB.display(window)

                    while fin:
                        Bouton_replay = Button('Rejouer', 200, 40, (100, 600), 5)
                        Bouton_quit = Button('Back to menu', 200, 40, (500, 600), 5)


                        white = (255, 255, 255)
                        window.fill(white)

                        if win:
                            text1 = font.render("Bravo vous avez vaincu votre adversaire", 1, grey)
                            window.blit(text1, (50, 300))
                            text2 = font.render("plus aucun pirates ne sillonne vos eaux", 1, grey)
                            window.blit(text2, (50, 400))
                        else:
                            text1 = font.render("Vous avez subi une defaite cuisante", 1, grey)
                            window.blit(text1, (50, 300))
                            text2 = font.render("mais cela n'est que partie remise", 1, grey)
                            window.blit(text2, (50, 400))

                        Bouton_quit.draw(window)
                        Bouton_replay.draw(window)
                        if Bouton_replay.pressed == True:
                            game = False
                            play = False
                            placement = False
                            button1.pressed = True
                            fin = False
                            menu = True
                        if Bouton_quit.pressed == True:
                            game = False
                            play = False
                            placement = False
                            fin = False
                            menu = True
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                run = False
                        pygame.display.update()

        # permet à l'utilisateur de quitter le jeu --> retour au menu principal
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # mise à jour de la fenetre
        pygame.display.update()


if __name__ == '__main__':
    main_NavalBattle()