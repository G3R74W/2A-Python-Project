import socket
import ping3 as ping



def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # on cree une socket vers une adresse qui n'a pas d' importance
        # puis on obtient le premier element du nom de la socket
        # cela nous donne notre IP
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def list_host (IP, min = 0, max = 255):
  # IP est une chaine sous la forme X1.X2.X3.X4
  # on coupe la chaine sur les points
  # puis on recupere les 3 premiers X pour avoir le reseau
  # une fois qu'on a le reseau on creer une liste
  #avec toutes possible les ip du reseau
  reseau= ""
  list_IP = IP.split(".")
  i=0
  for i in range(3):
    reseau += list_IP[i] + "."
  list_host = []
  print("RESEAU = %s"%(reseau))
  for j in range (min,max):
    host = reseau + "%s"%(j)
    list_host.append(host)
  return list_host



if __name__ == '__main__':
    IP = get_ip()
    print("mon IP est : %s"%(IP))
    list_IP = list_host(IP,15,20)
    print("la liste des hosts possible est : \n %s" %(list_IP))