# echo-server.py

import select    # replacement for input() with timeout
import socket    # sockets, obviously
import sys       # command-line arguments
import time      # time.sleep
import threading # multi-threading

HOST = "127.0.0.1"  # standard loopback interface address (localhost)
PORT = 16861        # port to listen on (non-privileged ports are > 1023)

# NOTE
# b'coucou'.decode('utf-8') =  'coucou'
#  'coucou'.encode('utf-8') = b'coucou'


# fonction qui cree un client avec des traces
# sortie = socket de communication
def createClient(host,port):
  newSocket = None
  try:
    newSocket = socket.create_connection((host,port))
    print("createClient, created client socket")
    
  except Exception as e:
    print("createClient failed (%s)" %(repr(e)))
  return newSocket

# fonction qui cree un serveur avec des traces
# sortie = socket d'ecoute
def createServer(host,port):
  newSocket = None
  try:
    newSocket = socket.create_server((host,port))
    print("createServer, created server socket")
    
  except Exception as e:
    print("createServer failed (%s)" %(repr(e)))
  return newSocket

# fonction qui gere la socket d'ecoute
# boucle limitee...
def serverListen(server,timeout,nIter=1):
  server.settimeout(timeout)
  iIter = 0
  newConnexion = None
  while iIter < nIter and not newConnexion:
    try:
      print("serverListen, listening (%d/%d), %.2fsec..." %(iIter+1,nIter,timeout))
      server.listen()
      newConnexion = server.accept()   #conn,addr = s.accept()
    except Exception as e:
      print("serverListen, timeout")
      iIter += 1
  print("serverListen, connected to (%s|%s)" %(newConnexion[0],newConnexion[1])) if newConnexion else print("serverListen, connection failed")
  return newConnexion

# fonction qui cree une socket de communication (mode serveur)
def server2():
  print("server2")
  connexion = None
  ecouteServer = createServer(HOST,PORT)
  if ecouteServer:
    (connexion,address) = serverListen(ecouteServer,6,20) # 2-minutes to connect
  print("server2, connexion=%s" %(repr(connexion)))
  return connexion

# fonction qui cree une socket de communication (mode client)
def client2():
  print("client2")
  connexion = createClient(HOST,PORT)
  print("client2, connexion=%s" %(repr(connexion)))
  return connexion


# objet de communication bi-directionnel
class Communicator():
  # methode: constructeur
  def __init__(self,connexion,name='Communicator'):
    self.name = name           # identifiant
    self.connexion = connexion # socket de communication
    self.listenThread  = None  # thread d'ecoute
    self.listenCB      = None  # fonction d'ecoute, reponse a la reception d'un message non vide
    self.listenData    = b''   # donnees recues
    self.messageThread = None  # thread d'entree de message
    self.messageFN     = None  # fonction d'entree de message
    self.messageData   = b''   # donnees d'entree
    self.sentData      = b''   # donnees envoyees (pour eviter les boucles infinies / echo)
    self.running = False       # etat de l'objet
    print("%20s | init, running <- %d" %(self.name,self.running))
  
  # methode: definition de la fonction d'ecoute
  def setCB_listen(self,function):
    self.listenCB = function
  
  # methode: definition de la fonction d'entree de message
  def setFN_message(self,function):
    self.messageFN = function
  
  # methode: demarrage du communicator
  def startCommunicator(self):
    if self.connexion:
      # on cree un thread pour l'ecoute
      if self.listenCB:
        print("%20s | start, creating listening thread" %(self.name))
        self.listenThread = threading.Thread(target=self.listenCB,args=(self,),daemon=True)
        self.listenThread.name = self.name+'_listeningThread'
      # on cree un thread pour l'entree de message
      if self.messageFN:
        print("%20s | start, creating message thread" %(self.name))
        self.messageThread = threading.Thread(target=self.messageFN,args=(self,),daemon=True)
        self.messageThread.name = self.name+'_messageThread'
      # go !
      self.running = True
      print("%20s | start : running <- %d" %(self.name,self.running))
    #
    if self.listenThread:
      self.listenThread.start()
    if self.messageThread:
      self.messageThread.start()

  # methode: envoi de message generique
  def sendData(self,data):
    print("%20s | sendData : running=%d" %(self.name,self.running))
    if self.running and data:
      #print("%20s | sendData (running OK)" %(self.name))
      try:
        if self.connexion and self.connexion.fileno() >= 0 :
          print("%20s | sendData, sending (%s)" %(self.name,repr(self.messageData)))
          self.sentData = data
          self.connexion.sendall(data)
        else:
          print("%20s | sendData, connexion lost, stop" %(self.name))
          self.running = False
          print("%20s | sendData, running <- %d" %(self.name,self.running))
      
      except Exception as e:
        print("%20s | sendData, error (%s)" %(self.name,repr(e)))
        self.running = False
        print("%20s | sendData, running <- %d" %(self.name,self.running))
    else:
      print("%20s | sendData (NOT running)" %(self.name))


# fonction d'entree de messages et d'envoi via un communicator... saisie clavier
def messageFN(communicator):
  print("| %20s    messageFN(%s)" %(threading.current_thread().name,communicator.name))
  # boucle eternelle (tant que le communicator tourne)
  while communicator.running:
    # <CLAVIER>
    print("| %20s    messageFN(%s) waiting..." %(threading.current_thread().name,communicator.name))
    data = input()
    print("> %s < INPUT" %repr(data))
    # message non vide...
    if data:
      # on encode pour passer d'une string a des donnes brutes
      communicator.messageData += data.encode('utf-8')
      print("| %20s    sending:(%s)" %(threading.current_thread().name,repr(communicator.messageData)))
      # envoi via la <SOCKET>
      communicator.sendData(communicator.messageData)
      # reinitialise les donnees d'envoi de l'objet
      communicator.messageData = b''

# fonction de reaction a un message recu via un communicator... socket echo
def actionFN(communicator):
  print("| %20s    actionFN(%s)" %(threading.current_thread().name,communicator.name))
  # boucle eternelle (tant que le communicator tourne)
  while communicator.running:
    # <SOCKET>
    print("| %20s    actionFN(%s) waiting..." %(threading.current_thread().name,communicator.name))
    data = communicator.connexion.recv(1024)
    # message non vide...
    if data:
      # on concatene les donnees recues
      communicator.listenData += data
      print("| %20s    received: %s [%s|%s]" %(threading.current_thread().name,repr(data),repr(communicator.listenData),repr(communicator.sentData)))
      # test pour eviter une boucle d'echo infinie
      if communicator.listenData == communicator.sentData:
        # on arrete l'echo
        communicator.sentData = b''
      else:
        # renvoi du message recu (ECHO)
        print("| %20s    sendecho: %s" %(threading.current_thread().name,repr(communicator.listenData)))
        communicator.sentData = communicator.listenData # pour pouvoir stopper la chose
        # envoi via la <SOCKET>
        communicator.connexion.sendall(communicator.listenData)
      # reinitialise les donnees d'ecoute de l'objet
      communicator.listenData = b''
      # gestion du message special 'STOP' pour mettre fin a la communication
      if data.decode('utf-8').lower()=='stop':
        communicator.running = False


# -- main --
if __name__=='__main__':
  print("__MAIN__")
  tArgs = sys.argv[1:]
  connexion = None
  communicator = None
  name = ''
  for ia,sa in enumerate(tArgs):
    print("    %-4d : %s" %(ia,sa))
  
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
    communicator = Communicator(connexion,name=name)
    communicator.setCB_listen(actionFN)
    communicator.setFN_message(messageFN)
    print("__MAIN__, starting communicator...")
    communicator.startCommunicator()
    print("__MAIN__, communicator started")
    while communicator.running:
      #print("__MAIN__, looping...")
      time.sleep(2)
    print("__MAIN__, communicator stopped")
    