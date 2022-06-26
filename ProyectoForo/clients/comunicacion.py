import socket, sys, json
from os import system, name
def clearS():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def sendT(sckt, srv, arg):     #Envia el mensaje codificado al bus de esta forma 00010sinitccsad
    if len(srv) < 5 or len(arg) < 1:
        print("Revisar argumentos")
        return
    lT = str(len(arg) + 5)
    while len(lT) < 5:
        lT = '0' + lT
    T = lT + srv + arg
    sckt.sendall(T.encode())

def listenB(sckt): #Retorna "sinit", "el contenido de la respuesta que brinda el bus(10 + 5) por ejemplo"
    
    amntRcvd = 0
    sT = None
    msgT = ''

    while True:
        data = sckt.recv(4096)
        if amntRcvd == 0:
            sT = int(data[:5].decode())
            nS = data[5:10].decode()
            msgT = msgT + data.decode()
            amntRcvd = amntRcvd + len(data)-5
        else:
            msgT = msgT + data.decode()
            amntRcvd = amntRcvd + len(data)
        if amntRcvd >= sT:
            break
    return nS, msgT