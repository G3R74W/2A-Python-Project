import select  # replacement for input() with timeout
import socket  # sockets, obviously
import sys  # command-line arguments
import time  # time.sleep
import threading  # multi-threading

HOST = "127.0.0.1"  # standard loopback interface address (localhost)
PORT = 16861  # port to listen on (non-privileged ports are > 1023)


# NOTE
# b'coucou'.decode('utf-8') =  'coucou'
#  'coucou'.encode('utf-8') = b'coucou'


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
def serverListen(server, timeout, nIter=1):
    server.settimeout(timeout)
    iIter = 0
    newConnexion = None
    while iIter < nIter and not newConnexion:
        #on ecoute durant un certain temps
        try:
            print("serverListen, listening (%d/%d), %.2fsec..." % (iIter + 1, nIter, timeout))
            server.listen()
            newConnexion = server.accept()
        except Exception as e:
            print("serverListen, timeout")
            iIter += 1
    print("serverListen, connected to (%s|%s)" % (newConnexion[0], newConnexion[1])) if newConnexion else print(
        "serverListen, connection failed")
    #si on ne c'est pas connecte pendant ce temps on return None
    #si on c'est connecte on return la un tuple contenant la socket et l'adresse qui c'est connecte
    return newConnexion


# fonction qui cree une socket de communication (mode serveur)
def server2():
    print("server2")
    connexion = None
    ecouteServer = createServer(HOST, PORT)
    if ecouteServer:
        (connexion, address) = serverListen(ecouteServer, 6, 20)
    print("server2, connexion=%s" % (repr(connexion)))
    return connexion


# fonction qui cree une socket de communication (mode client)
def client2():
    print("client2")
    connexion = createClient(HOST, PORT)
    print("client2, connexion=%s" % (repr(connexion)))
    return connexion


# objet de communication bi-directionnel
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
    return input().encode('utf-8')


def reaction(objet, data):
    print("|\n|\n| %s\n|\n|\n" % (repr(data)))


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

# -- main --
if __name__ == '__main__':
    ip_main()