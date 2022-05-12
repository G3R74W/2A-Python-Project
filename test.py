# echo-server.py

import socket
import threading
import sys
import ping3 as ping

HOST = "192.168.43.89"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


def server_echo():
    print(f"server_echo: BEGIN")
    bLoop1 = True
    while bLoop1:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))  # on ouvre le port de communication special
            print(f"server_echo: (listen)")
            s.listen()  # on attend que qqln ce connecte
            conn, addr = s.accept()  # on accept ca connection
            with conn:
                # on verifie que c'est bien notre application
                data = conn.recv(1024)
                sData = data.decode('utf-8')
                print(f"server_echo: Received {sData}")
                if sData == 'Test-Serveur':
                    verif = "ok"
                    conn.sendall(verif.encode("utf-8"))
                    print(f"server_echo: Connected by {addr}")
                    # on attend les message de l'utilisateur on le decode, l'ecrit
                    # l'interpret, et on le revoie
                    while True:
                        data = conn.recv(1024)
                        sData = data.decode('utf-8')
                        print(f"server_echo: Received {sData}")
                        # print(f"server_echo: Received {data!r}")
                        if not data:
                            print(f"server_echo: no data")
                            break
                        elif sData == 'stop':
                            print(f"server_echo: (STOP)")
                            bLoop1 = False
                            break
                        conn.sendall(data)
                else:
                    refus = "Le message d'autentification n'est pas le bon"
                    print(refus)
                    conn.sendall(refus.encode("utf-8"))
                print(f"server_echo: loop ended")
            print(f"server_echo: connexion closed")
        print(f"server_echo: ...")
    print(f"server_echo: END")


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # on cree une socket vers une adresse qui n'a pas d'importance
        # puis on chope le premier element du nom de la socket
        # cela nous donne notre IP
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def list_host(IP):
    # IP est une chaine sous la forme X1.X2.X3.X4
    # on coupe la chaine sur les points
    # puis on recupere les 3 premiers X pour avoir le reseau
    # une fois qu'on a le reseau on creer une liste
    # avec toutes possible les ip du reseau
    reseau = ""
    list_IP = IP.split(".")
    i = 0
    for i in range(3):
        reseau += list_IP[i] + "."
    list_host = []
    print("RESEAU = %s" % (reseau))
    for j in range(87, 90):
        host = reseau + "%s" % (j)
        list_host.append(host)
    return list_host


def test_ping(list_host):
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
        server_echo()
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
                    data = test_socket.recv(1024)
                    print("message recu : %s" % (data.decode("utf-8")))
                except Exception as e:
                    print("erreur dans l'envoie du message \n -> erreur : %s" % (e))
                    conversation = False

        except Exception as e:
            print("erreur de connection avec l'hote \n -> erreur : %s" % (e))


if __name__ == '__main__':
    IP = get_ip()
    print(IP)
    list_host = list_host(IP)
    ##print(list_host)
    test_ping(list_host)