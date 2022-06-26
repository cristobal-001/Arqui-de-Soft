import socket, json
from db_uci import dbuci
from comunicacion import sendT, listenB, registerS
srv = 'ccdsu'

#Registrar usuario
def registerU(rgtr): #Parametro de entrada OKccdsu
    crsr = dbuci.cursor()
    crsr.execute("SELECT username FROM users WHERE username = %s", (rgtr["username"],))
    fetched = crsr.fetchone()
    if fetched == None:
        if rgtr["rol"] in ["1","2"]:
            #rol = "administrador" if rgtr["rol"] == "1" else "general"
            crsr.execute("INSERT INTO users (username, password, rol) VALUES(%s, %s, %s)", (rgtr["username"],rgtr["password"], rgtr["rol"]))
            dbuci.commit()
            response = {"respuesta":"El usuario ha sido registrado exitosamente."}
            sendT(sckt, srv, json.dumps(response))
        else:
            response = {"respuesta":"No se ha podido registrar al usuario."}
            sendT(sckt, srv, json.dumps(response))
    else:
        response = {"respuesta":"El usuario introducido ya se encuentra registrado."}
        sendT(sckt, srv, json.dumps(response))



if __name__ == "__main__":
    try:
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_address = ('localhost', 5000)
        print('Servicio: Conectándose a {} puerto {}'.format(*server_address))
        sckt.connect(server_address)
    except:
        print('No es posible la conexión al bus')
        quit()

    registerS(sckt, srv) #Activa el servicio

    while True:
        nS, mT = listenB(sckt)
        if nS == srv:
            print(mT)
            registerU(rgtr=json.loads(mT))
        else:
            response = {"respuesta":"servicio incorrecto"}
            sendT(sckt, srv, json.dumps(response))

    print('Se cierra socket')
    sckt.close()