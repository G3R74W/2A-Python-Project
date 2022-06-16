# -*- coding: UTF-8 -*-
import pygame
from pygame import *
import Button
from Button import *
import InputBox
from InputBox import *
import time
import select  # replacement for input() with timeout
import socket  # sockets, obviously
import sys  # command-line arguments
import threading  # multi-threading

HOST = "127.0.0.1"  # standard loopback interface address (localhost)
PORT = 16861  # port to listen on (non-privileged ports are > 1023)


# NOTE
# b'coucou'.decode('utf-8') =  'coucou'
#  'coucou'.encode('utf-8') = b'coucou'


def window_init():
    """initialisation de la fenêtre"""
    # initialisation pygame
    pygame.init()
    window = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("CHAT")
    window_refresh(window)
    return window


def window_refresh(window):
    """permet de refresh la fenêtre"""
    window.fill((50, 90, 168))


def button_creation():
    """creation des differents bouttons"""
    button1 = Button('Back to menu', 200, 40, (290, 670), 5)
    button2 = Button('Send', 200, 40, (600, 680), 5)
    button3 = Button('^', 20, 20, (100, 670), 5)
    button4 = Button('v', 20, 20, (100, 700), 5)
    return button1, button2, button3, button4


def message_content():
    """permet l'attribution du contenu du fichier.txt contenant l'entièreté des messages"""
    AllMessages = open('messages.txt', 'r')
    content = AllMessages.readlines()
    AllMessages.close()
    return content


def message_display(window, content, counter):
    """permet d'afficher les messages précédents dans le chat"""
    xPos = 550
    nbr_message = len(content)
    width = 230

    # on peut afficher maximum 12 messages sur l'écran
    # on test si il y a plus de 12 messages dans le fichiers
    if nbr_message > 12:
        depassement = nbr_message - 12
        yPos = counter * 50 - depassement * 50
    else:
        yPos = 50

    # on fait en sorte de ne pas afficher les messages au délà du cadre prévu
    if counter > 1:
        msgRange = len(content) - counter
    else:
        msgRange = len(content)

    for i in range(msgRange):
        # on initialise le compteur de caractères par ligne à 0
        car_counter = 0

        # hauteur du rectangle qui entour le message
        height = 30

        # on supprime le caractère de retour chariot pour qu'il ne s'affiche pas dans pygame
        msgLength = len(content[i]) - 1
        message = ""

        # on identifie l'envoyeur à partir du code placé au début du message
        # 0 si le message est envoyé par nous
        # 1 si le message est envoyé par l'autre utilisateur
        if content[i][0] == "0":
            xPos = 550
            sender = "you:"
            msgColor = (50, 168, 131)
        elif content[i][0] == "1":
            xPos = 50
            sender = "other:"
            msgColor = (162, 166, 168)

        # on retire le code devant le message qui permet d'identifier l'envoyeur
        for j in range(msgLength):
            if content[i][j] == "0" or content[i][j] == "1":
                message += ""
            else:
                message += content[i][j]
            # compteur de caractère par ligne
            car_counter += 1
            if car_counter == 19:
                car_counter = 0
                height += 50

        if message != "\n" and message != "":
            pygame.draw.rect(window, msgColor, (xPos - 10, yPos - 5, width, height), border_radius=4)
        text = font.render(message, 1, (0, 0, 0))
        window.blit(text, (xPos, yPos))

        yPos += 50


# fonction qui cree un client avec des traces
# sortie = socket de communication
def createClient(host, port):
    newSocket = None
    try:
        newSocket = socket.create_connection((host, port))
        print("createClient, created client socket")

    except Exception as e:
        print("createClient failed (%s)" % (repr(e)))
    return newSocket


# fonction qui cree un serveur avec des traces
# sortie = socket d'ecoute
def createServer(host, port):
    newSocket = None
    try:
        newSocket = socket.create_server((host, port))
        print("createServer, created server socket")

    except Exception as e:
        print("createServer failed (%s)" % (repr(e)))
    return newSocket

# fonction qui gere la socket d'ecoute
# boucle limitee...
def serverListen(server, timeout, nIter=1):
    server.settimeout(timeout)
    iIter = 0
    newConnexion = None
    while iIter < nIter and not newConnexion:
        try:
            print("serverListen, listening (%d/%d), %.2fsec..." % (iIter + 1, nIter, timeout))
            server.listen()
            newConnexion = server.accept()  # conn,addr = s.accept()
        except Exception as e:
            print("serverListen, timeout")
            iIter += 1
    print("serverListen, connected to (%s|%s)" % (newConnexion[0], newConnexion[1])) if newConnexion else print(
        "serverListen, connection failed")
    return newConnexion


# fonction qui cree une socket de communication (mode serveur)
def server2():
    print("server2")
    connexion = None
    ecouteServer = createServer(HOST, PORT)
    if ecouteServer:
        (connexion, address) = serverListen(ecouteServer, 6, 20)  # 2-minutes to connect
    print("server2, connexion=%s" % (repr(connexion)))
    return connexion


# fonction qui cree une socket de communication (mode client)
def client2():
    print("client2")
    connexion = createClient(HOST, PORT)
    print("client2, connexion=%s" % (repr(connexion)))
    return connexion


class Communicator():
    # methode: constructeur
    def __init__(self, connexion, name='Communicator'):
        self.name = name  # identifiant
        self.connexion = connexion  # socket de communication
        self.entreeFonction = None
        self.entreeFonctionObject = None
        self.reactionFonction = None
        self.reactionFonctionObject = None
        self.running = False  # etat de l'objet
        print("%20s | init, running <- %d" % (self.name, self.running))

    # methode: definition de la fonction d'entree
    def setEntreeFonction(self, function, object):
        self.entreeFonction = function
        self.entreeFonctionObject = object

    # methode: definition de la fonction d'ecoute
    def setReactionFonction(self, function, object):
        self.reactionFonction = function
        self.reactionFonctionObject = object

    # methode: demarrage du communicator
    def startCommunicator(self):
        if self.connexion:
            # on cree un thread pour l'ecoute
            print("%20s | start, creating listening thread" % (self.name))
            listenThread = threading.Thread(target=Communicator.listenLoop,
                                            args=(self, self.reactionFonction, self.reactionFonctionObject,),
                                            daemon=True)
            listenThread.name = self.name + '_listeningThread'
            # on cree un thread pour l'entree de message
            print("%20s | start, creating message thread" % (self.name))
            messageThread = threading.Thread(target=Communicator.messageLoop,
                                             args=(self, self.entreeFonction, self.entreeFonctionObject,), daemon=True)
            messageThread.name = self.name + '_messageThread'
            # go !
            self.running = True
            print("%20s | start : running <- %d" % (self.name, self.running))
        #
        if listenThread:
            listenThread.start()
        if messageThread:
            messageThread.start()

    # methode: envoi de message generique
    def sendData(self, data):
        print("%20s | sendData : running=%d" % (self.name, self.running))
        if self.running and data:
            # print("%20s | sendData (running OK)" %(self.name))
            try:
                if self.connexion and self.connexion.fileno() >= 0:
                    print("%20s | sendData, sending (%s)" % (self.name, repr(data)))
                    # self.sentData = data
                    self.connexion.sendall(data)
                else:
                    print("%20s | sendData, connexion lost, stop" % (self.name))
                    self.running = False
                    print("%20s | sendData, running <- %d" % (self.name, self.running))

            except Exception as e:
                print("%20s | sendData, error (%s)" % (self.name, repr(e)))
                self.running = False
                print("%20s | sendData, running <- %d" % (self.name, self.running))
        else:
            print("%20s | sendData (NOT running)" % (self.name))

    # boucle sur fonction d'entree de messages et d'envoi
    def messageLoop(self, function, functionObject):
        print("| %20s    messageLoop(%s)" % (threading.current_thread().name, self.name))
        # boucle eternelle (tant que le communicator tourne)
        while self.running:
            print("| %20s    messageLoop(%s) waiting..." % (threading.current_thread().name, self.name))
            # data = input().encode('utf-8')
            data = function(functionObject)
            print("> %s < INPUT" % repr(data)) if data else None
            # message non vide...
            if data:
                # on encode pour passer d'une string a des donnes brutes
                print("| %20s    messageLoop: sending:(%s)" % (threading.current_thread().name, repr(data)))
                # envoi via la <SOCKET>
                self.sendData(data)

    # fonction de reaction a un message recu via un communicator... socket echo
    def listenLoop(self, function, functionObject):
        print("| %20s    listenLoop(%s)" % (threading.current_thread().name, self.name))
        # boucle eternelle (tant que le communicator tourne)
        while self.running:
            # <SOCKET>
            print("| %20s    listenLoop(%s) waiting..." % (threading.current_thread().name, self.name))
            data = self.connexion.recv(1024)
            # message non vide...
            if data:
                # on concatene les donnees recues
                print("\n| %20s    listenLoop received: [%s]\n" % (threading.current_thread().name, repr(data)))
                # gestion du message special 'STOP' pour mettre fin a la communication
                if data.decode('utf-8').lower() == 'stop':
                    self.sendData(b'stop')
                    self.running = False
                elif function:
                    function(functionObject, data)



def entree(objet):
    AllMessage = open('messages.txt', 'r')
    msgList = AllMessage.readlines()
    # longueur de la liste
    nbMsg = len(msgList)
    message = str(msgList[nbMsg - 1])
    #message = "message de debug"
    print("message : %s"%(message))
    AllMessage.close()
    print("ENTREE DANS LA FONCTION")
    send = False
    lastNumber = open('numberMessage.txt', 'r')
    lstNumber = lastNumber.read()

    if lstNumber == "":
        lstNumber = "0"

    print("le contenue du numberMessage.txt est : \n %s"%(lstNumber))
    numlstNumber = int(lstNumber)

    print("il y a %s messages et le dernier est %s " %(nbMsg,numlstNumber))

    if numlstNumber < nbMsg:
        lastNumber.close()
        reouverture = open('numberMessage.txt', 'w')
        print(str(nbMsg))
        reouverture.write(str(nbMsg))
        reouverture.close()
        send = True
    else:
        send = False
        lastNumber.close()

    if send:
        print("envoie du message : %s"%(message))
        return message.encode("utf-8")
    else:
        print("envoie vide normalement")
        return None

def reaction(objet,data):
    print("j'entre dans la reaction")
    car_counter = 0
    data = data.decode("utf-8")
    if data != "\n":
        print("REACTION data recu = :%s:"%(data))
        AllMessage = open('messages.txt', 'a')
        AllMessage.write("1")
        for k in range(len(data)):
            AllMessage.write(str(data[k]))
            car_counter += 1
            if car_counter == 19:
                AllMessage.write("\n" + '1')
                car_counter = 0
        AllMessage.write('\n')


def ip_main():
    print("__MAIN__")
    tArgs = sys.argv[1:]
    connexion = None
    communicator = None
    name = ''
    for ia, sa in enumerate(tArgs):
        print("    %-4d : %s" % (ia, sa))

    if 's' in sys.argv:
        # > python sock03.py s
        print("SERVER")
        connexion = server2()
        name = 'server'
    else:
        # > python sock03.py
        print("CLIENT")
        connexion = client2()
        name = 'client'

    if connexion:
        print("__MAIN__, create communicator...")
        communicator = Communicator(connexion, name=name)
        communicator.setEntreeFonction(entree, None)
        communicator.setReactionFonction(reaction, None)
        print("__MAIN__, starting communicator...")
        communicator.startCommunicator()
        print("__MAIN__, communicator started")
        while communicator.running:
            # print("__MAIN__, looping...")
            time.sleep(2)
        print("__MAIN__, communicator stopped")


def main_chat():
    """main du chat"""
    window = window_init()
    window_init()
    clock = pygame.time.Clock()

    button1, button2, button3, button4 = button_creation()

    # colors
    white = (255, 255, 255)

    print("__MAIN__")
    tArgs = sys.argv[1:]
    connexion = None
    communicator = None
    name = ''
    for ia, sa in enumerate(tArgs):
        print("    %-4d : %s" % (ia, sa))

    if 's' in sys.argv:
        # > python sock03.py s
        print("SERVER")
        connexion = server2()
        name = 'server'
    else:
        # > python sock03.py
        print("CLIENT")
        connexion = client2()
        name = 'client'

    if connexion:
        print("__MAIN__, create communicator...")
        communicator = Communicator(connexion, name=name)
        communicator.setEntreeFonction(entree, None)
        communicator.setReactionFonction(reaction, None)
        print("__MAIN__, starting communicator...")
        communicator.startCommunicator()
        print("__MAIN__, communicator started")

    # input box
    inputBox = InputBox()
    boxlist = [inputBox]

    # booleans
    run = True

    counter = 1
    while run:
        # button1.draw(window)

        content = message_content()

        pygame.draw.rect(window, (99, 137, 153), (0, 0, 800, 650))
        button2.draw(window)
        button3.draw(window)
        button4.draw(window)

        if button1.pressed == True:
            print('back to main menu')
            button1.pressed = False
            run = False

        if button3.pressed == True:
            print('up')
            time.sleep(0.2)
            button3.pressed = False
            counter += 1

        if button4.pressed == True:
            print('down')
            time.sleep(0.2)
            button4.pressed = False
            counter -= 1

        for event in pygame.event.get():
            for box in boxlist:
                message = box.handle_event(event, window)
                # compteur de caractères
                car_counter = 0
                if message != '':
                    AllMessage = open('messages.txt', 'a')
                    AllMessage.write("0")
                    for k in range(len(message)):
                        AllMessage.write(message[k])
                        car_counter += 1
                        if car_counter == 19:
                            AllMessage.write("\n" + '0')
                            car_counter = 0

                    AllMessage.write('\n')
                    box.message = ''
                    AllMessage.close()

            # permet à l'utilisateur de quitter le jeu --> retour au menu principal
            if event.type == pygame.QUIT:
                run = False
        content = message_content()

        message_display(window, content, counter)

        pygame.display.update()
        inputBox.update()
        window_refresh(window)
        inputBox.draw(window)
