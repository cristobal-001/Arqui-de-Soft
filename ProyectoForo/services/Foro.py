import socket, json
import comunicacion as com
import socket, json
from db_uci import dbuci
from comunicacion import sendT, listenB, registerS

srv = "postr"


def Agregar_post(mensaje):
    crsr = dbuci.cursor(buffered = True)
    crsr.execute("SELECT usuario_id FROM Usuario WHERE nombre = %s", (mensaje["nombre"],))
    fetched = crsr.fetchone()[0]
    crsr.execute("INSERT INTO Hilo (usuario_id, categoria_id, contenido, es_anonimo, esta_abierto) VALUES(%s,%s,%s,%s,%s)", (fetched,mensaje["categoria_id"],mensaje["contenido"],mensaje["es_anonimo"],1))
    dbuci.commit()
    sendT(sckt,srv,"Post agregado")
    return


if __name__ == "__main__":
    try:
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Crea socket

        direccion = ('localhost', 5000)
        print('Servicio: Conectándose a {} puerto {}'.format(*direccion))
        sckt.connect(direccion)
    except:
        print('No es posible la conexión al bus')
        quit()

    com.registerS(sckt,'postr') #Inicia el servicio comentar

    while True:
        nS, mT = com.listenB(sckt) #A la espera del Bus
        if nS == 'postr':
            print("Contenido : ", mT , "  Nombre del servicio :",nS)
            Agregar_post(mensaje=json.loads(mT))
        else:
            print(nS)
            response = {"Respuesta":"error nombre del servicio"}
            com.sendT(sckt, 'comen', json.dumps(response))

